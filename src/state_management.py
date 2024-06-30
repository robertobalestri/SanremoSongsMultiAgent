import os
import pandas as pd
import streamlit as st
import zipfile
from io import BytesIO
from config import BASE_EXTRACTED_DIR, DATABASE_ZIP_CANZONI_DIR, DEFAULT_SONG_NAME, DEFAULT_BREVE_BIO, DEFAULT_TEMA_CANZONE
from crew.crew import main_crew
from src.llms_not_in_crew import regenerate_lines
from src.utils import save_user_input, check_existing_files, load_existing_files, flush_existing_files, save_expanded_biography, save_generated_themes, save_corrected_song_lines, save_music_description

def initialize_session_state():
    if 'expanded_biography' not in st.session_state:
        st.session_state.expanded_biography = ""
    if 'generated_themes' not in st.session_state:
        st.session_state.generated_themes = ""
    if 'song_lines' not in st.session_state:
        st.session_state.song_lines = {}
    if 'music_description' not in st.session_state:
        st.session_state.music_description = ""
    if 'last_update_time' not in st.session_state:
        st.session_state.last_update_time = 0
    if 'grid_data' not in st.session_state:
        st.session_state.grid_data = pd.DataFrame()
    if 'first_run' not in st.session_state:
        st.session_state.first_run = True
    if 'editor_content' not in st.session_state:
        st.session_state.editor_content = ""
    if 'zip_processed' not in st.session_state:
        st.session_state.zip_processed = False
    if 'selected_zip' not in st.session_state:
        st.session_state.selected_zip = None
    if 'breve_biografia' not in st.session_state:
        st.session_state.breve_biografia = DEFAULT_BREVE_BIO
    if 'tema' not in st.session_state:
        st.session_state.tema = DEFAULT_TEMA_CANZONE

def reset_checkboxes():
    for i in st.session_state.song_lines:
        st.session_state.song_lines[i]['to_regenerate'] = False

def read_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

def generate_song_files(breve_biografia, tema):
    with st.spinner("Generazione della canzone in corso..."):
        if not (check_existing_files()):
            result = main_crew.kickoff(inputs={"topic": breve_biografia, "theme": tema})
            save_user_input(breve_biografia, tema)

    return load_existing_files()

def generate_song(breve_biografia, tema):
    expanded_biography, generated_themes, corrected_song_lines, music_description, user_input = generate_song_files(breve_biografia, tema)
    update_session(
        expanded_biography=expanded_biography,
        generated_themes=generated_themes,
        song_lines={
            i: {"original": line.strip(), "current": line.strip(), "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
            for i, line in enumerate(corrected_song_lines)
        },
        music_description=music_description,
        first_run=False,
        editor_content="\n".join([line.strip() for line in corrected_song_lines])
    )
    # Update session state for breve_biografia and tema to retain user input
    st.session_state.breve_biografia = breve_biografia
    st.session_state.tema = tema

def update_session(**kwargs):
    for key, value in kwargs.items():
        st.session_state[key] = value

def update_session_state_from_grid(grid_data):
    reordered_song_lines = {}
    for new_index, (_, row) in enumerate(grid_data.iterrows()):
        i = int(row['Index'])
        reordered_song_lines[new_index] = st.session_state.song_lines[i]
        reordered_song_lines[new_index]['current'] = row['Line']
        reordered_song_lines[new_index]['to_regenerate'] = row['Regenerate']
    update_session(
        song_lines=reordered_song_lines,
        editor_content="\n".join([line_data['current'] for line_data in reordered_song_lines.values()])
    )

def regenerate_selected_lines():
    with st.spinner("Rigenerazione delle frasi in corso..."):
        lyrics = "\n".join([line_data["original"] for line_data in st.session_state.song_lines.values()])
        consecutive_groups = []
        current_group = []
        for i, line_data in st.session_state.song_lines.items():
            if line_data["to_regenerate"]:
                current_group.append(line_data["current"])
            elif current_group:
                consecutive_groups.append(current_group)
                current_group = []
        if current_group:
            consecutive_groups.append(current_group)
        for group in consecutive_groups:
            regenerated_lines = regenerate_lines(group, lyrics)
            for original_line, new_line in zip(group, regenerated_lines):
                for i, line_data in st.session_state.song_lines.items():
                    if line_data["current"] == original_line:
                        line_data["current"] = new_line
                        line_data["regeneration_count"] += 1
                        line_data["to_be_green"] = True
                        line_data["to_regenerate"] = False

def handle_zip_upload(uploaded_zip):
    # Save the uploaded ZIP file in the database directory
    zip_path = os.path.join(DATABASE_ZIP_CANZONI_DIR, uploaded_zip.name)
    with open(zip_path, 'wb') as f:
        f.write(uploaded_zip.getvalue())

    # Extract the contents of the ZIP file into the extracted directory
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(BASE_EXTRACTED_DIR)

    if check_existing_files():
        if existing_files := load_existing_files():
            expanded_biography, generated_themes, corrected_song_lines, music_description, user_input = existing_files
            update_session(
                expanded_biography=expanded_biography,
                generated_themes=generated_themes,
                song_lines={
                    i: {"original": line.strip(), "current": line.strip(), "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
                    for i, line in enumerate(corrected_song_lines)
                },
                music_description=music_description,
                editor_content="\n".join([line.strip() for line in corrected_song_lines]),
                grid_data=pd.DataFrame([{"Index": i, "Line": line.strip(), "Regenerate": False} for i, line in enumerate(corrected_song_lines)]),
                first_run=False
            )

def save_song_to_zip(zip_name):
    save_expanded_biography(st.session_state.expanded_biography)
    save_generated_themes(st.session_state.generated_themes)
    save_corrected_song_lines([line_data['current'] for line_data in st.session_state.song_lines.values()])
    save_music_description(st.session_state.music_description)
    with BytesIO() as buffer:
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, subfolders, filenames in os.walk(BASE_EXTRACTED_DIR):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, os.path.relpath(file_path, BASE_EXTRACTED_DIR))
        buffer.seek(0)
        with open(os.path.join(DATABASE_ZIP_CANZONI_DIR, f"{zip_name}.zip"), 'wb') as f:
            f.write(buffer.read())

def initialize_and_load_state():
    #flush_existing_files()
    initialize_session_state()
    
    if 'zip_processed' in st.session_state and st.session_state.zip_processed:
        if st.session_state.first_run and check_existing_files():
            if existing_files := load_existing_files():
                expanded_biography, generated_themes, corrected_song_lines, music_description, user_input = existing_files
                update_session(
                    expanded_biography=expanded_biography,
                    generated_themes=generated_themes,
                    song_lines={
                        i: {"original": line.strip(), "current": line.strip(), "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
                        for i, line in enumerate(corrected_song_lines)
                    },
                    music_description=music_description,
                    editor_content="\n".join([line.strip() for line in corrected_song_lines]),
                    grid_data=pd.DataFrame([{"Index": i, "Line": line.strip(), "Regenerate": False} for i, line in enumerate(corrected_song_lines)]),
                    first_run=False
                )
