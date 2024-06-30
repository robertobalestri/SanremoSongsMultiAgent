import streamlit as st
import pandas as pd
import os
import zipfile
from io import BytesIO
from config import BASE_EXTRACTED_DIR, DATABASE_ZIP_CANZONI_DIR, DEFAULT_SONG_NAME
from crew.crew import main_crew
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, AgGridTheme
from streamlit_monaco import st_monaco
from src.utils import check_existing_files, load_existing_files, flush_existing_files
from src.state_management import reset_checkboxes, generate_song, update_session_state_from_grid, regenerate_selected_lines, handle_zip_upload, save_song_to_zip, initialize_and_load_state, update_session

# Set page configuration for wide layout
st.set_page_config(layout="wide")

# CSS for custom styling
st.markdown("""
    <style>
        .lyrics-container {
            font-family: 'Courier New', Courier, monospace;
            white-space: pre-wrap; /* Preserve whitespace */
            background: #f4f4f4; /* Light grey background */
            padding: 20px; /* Some padding for better readability */
            border-radius: 10px; /* Rounded corners */
            border: 1px solid #ddd; /* Light border */
            overflow-y: auto; /* Enable vertical scrolling if needed */
            height: 100%;
            color: #333; /* Dark text color */
        }
        .lyrics-container p {
            margin: 0; /* Remove default paragraph margin */
            line-height: 1.5; /* Improve line spacing */
        }
    </style>
""", unsafe_allow_html=True)

def list_zip_files():
    return [f for f in os.listdir(DATABASE_ZIP_CANZONI_DIR) if f.endswith('.zip')]

def display_generated_song():
    st.sidebar.write("### Biografia Espansa")
    st.sidebar.write(st.session_state.expanded_biography)
    st.sidebar.write("### Tema della canzone")
    st.sidebar.write(st.session_state.generated_themes)
    st.sidebar.write("### Descrizione Musicale")
    st.sidebar.write(st.session_state.music_description)
    st.sidebar.write("Vai qui e crea il brano: [Crea il brano](https://suno.com/create)")

    default_zip_name = st.session_state.get('selected_zip', DEFAULT_SONG_NAME).replace('.zip', '')
    
    col1, col2, col_empty = st.columns([3, 1, 2])
    with col1:
        zip_name = st.text_input(label="", value=default_zip_name, label_visibility='collapsed')
    with col2:
        if st.button("Save Song", type='primary'):
            save_song_to_zip(zip_name)

    col1, col2 = st.columns([3, 2])

    with col1:
        col1x, col1empty, col1y = st.columns([1, 2, 1])

        with col1y:
            if st.button("Rigenera Frasi"):
                regenerate_selected_lines()
                reset_checkboxes()
                st.rerun()
  
        song_lines = [{"Index": i, "Line": f"{line_data['current']}", "Regenerate": line_data['to_regenerate']} for i, line_data in st.session_state.song_lines.items()]
        df = pd.DataFrame(song_lines)

        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_column("Index", rowDrag=True, rowDragManaged=True, headerCheckboxSelection=False, checkboxSelection=False, width=100, suppressMovable=True, sortable=False)
        gb.configure_column("Line", editable=True, singleClickEdit=True, flex=1, suppressMovable=True, sortable=False)
        gb.configure_column("Regenerate", headerCheckboxSelection=False, editable=True, width=100, suppressMovable=True, sortable=False)
        gb.configure_grid_options(rowDragManaged=True, autoSizeStrategy='fitGridWidth', headerHeight = 0)

        grid_options = gb.build()

        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=1200,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=True,
            theme=AgGridTheme.STREAMLIT,
            update_on=['rowDragEnd', 'cellValueChanged'],
        )

        grid_data = pd.DataFrame(grid_response['data'])

        if not grid_data.equals(st.session_state.grid_data):
            st.session_state.grid_data = grid_data
            st.session_state.grid_changed = True
        else:
            st.session_state.grid_changed = False

        update_session_state_from_grid(grid_data)

        if st.session_state.grid_changed:
            st.rerun()

    with col2:
        update_lyrics_button = st.button("Update Lyrics")
        content = st_monaco(value=st.session_state.editor_content, height="1200px", language="plaintext", theme="vs-light")

        if update_lyrics_button:
            updated_lines = content.split("\n")
            update_session(
                editor_content=content,
                song_lines={
                    i: {"original": line, "current": line, "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
                    for i, line in enumerate(updated_lines)
                },
                grid_data=pd.DataFrame([{"Index": i, "Line": line, "Regenerate": False} for i, line in enumerate(updated_lines)])
            )
            st.rerun()

def handle_uploaded_zip():
    uploaded_zip = st.sidebar.file_uploader("Upload ZIP file", type=["zip"])
    
    if st.sidebar.button("Load Saved Song", type='primary'):
        update_session(zip_processed=False)
        st.rerun()
        
    if uploaded_zip is not None and not st.session_state.zip_processed:
        flush_existing_files()
        handle_zip_upload(uploaded_zip)
        update_session(zip_processed=True)
        st.sidebar.success("Files extracted successfully!")

def handle_zip_selection(selected_zip):
    zip_path = os.path.join(DATABASE_ZIP_CANZONI_DIR, selected_zip)
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
                first_run=False,
                selected_zip=selected_zip
            )

def main():
    initialize_and_load_state()

    st.sidebar.title("Song Database")
    zip_files = list_zip_files()
    selected_zip = st.sidebar.selectbox("Select a ZIP file to load", zip_files)
    if st.sidebar.button("Load Selected ZIP"):
        handle_zip_selection(selected_zip)
    
    handle_uploaded_zip()
    
    if st.session_state.first_run:
        st.title("Generatore di Canzoni")
        st.write("Inserisci una breve biografia del musicista e lascia che il nostro sistema crei una canzone personalizzata per te.")
        breve_biografia = st.text_area("Breve Biografia", value="Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo")
        tema = st.text_area("Tema", value="Cosa vuol dire essere ex trans, solo metafore stupide")
        generate_button = st.button("Genera Canzone")
        if generate_button:
            generate_song(breve_biografia, tema)
    else:
        with st.sidebar:
            st.title("Generatore di Canzoni")
            st.write("Inserisci una breve biografia del musicista e lascia che il nostro sistema crei una canzone personalizzata per te.")
            breve_biografia = st.text_area("Breve Biografia", value="Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo")
            tema = st.text_area("Tema", value="Cosa vuol dire essere ex trans, solo metafore stupide")
            generate_button = st.button("Genera Altra Canzone")
            if generate_button:
                flush_existing_files()
                generate_song(breve_biografia, tema)

    if st.session_state.song_lines:
        display_generated_song()

if __name__ == "__main__":
    main()