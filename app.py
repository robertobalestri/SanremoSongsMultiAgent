import streamlit as st
import pandas as pd
from config import IS_LOCAL, EXPANDED_BIOGRAPFY_OUTPUT_PATH, GENERATED_THEMES_PATH, CORRECTED_SONG_PATH, MUSIC_DESCRIPTION_OUTPUT_PATH
from crew.crew import main_crew
from src.llms_not_in_crew import regenerate_lines
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, AgGridTheme
from streamlit_monaco import st_monaco

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

# Initialize session state variables
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

def reset_checkboxes():
    for i in st.session_state.song_lines:
        st.session_state.song_lines[i]['to_regenerate'] = False

@st.cache_data
def read_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()

@st.cache_data
def generate_song_files(breve_biografia, tema):
    with st.spinner("Generazione della canzone in corso..."):
        # Simulate generating the song and related data
        #result = main_crew.kickoff(inputs={"topic": breve_biografia, "theme": tema})
        pass
    expanded_biography_output_path = EXPANDED_BIOGRAPFY_OUTPUT_PATH
    generated_themes_path = GENERATED_THEMES_PATH
    corrected_song_path = CORRECTED_SONG_PATH
    music_description_output_path = MUSIC_DESCRIPTION_OUTPUT_PATH

    return (
        read_file(expanded_biography_output_path),
        read_file(generated_themes_path),
        read_file(corrected_song_path).splitlines(),
        read_file(music_description_output_path)
    )

def generate_song(breve_biografia, tema):
    expanded_biography, generated_themes, corrected_song_lines, music_description = generate_song_files(breve_biografia, tema)

    st.session_state.expanded_biography = expanded_biography
    st.session_state.generated_themes = generated_themes
    st.session_state.song_lines = {
        i: {"original": line.strip(), "current": line.strip(), "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
        for i, line in enumerate(corrected_song_lines)
    }
    st.session_state.music_description = music_description
    st.session_state.first_run = False  # Set first_run to False after generating the song
    st.session_state.editor_content = "\n".join([line_data['current'] for line_data in st.session_state.song_lines.values()])

def update_session_state_from_grid(grid_data):
    reordered_song_lines = {}
    for new_index, (_, row) in enumerate(grid_data.iterrows()):
        i = int(row['Index'])
        reordered_song_lines[new_index] = st.session_state.song_lines[i]
        reordered_song_lines[new_index]['current'] = row['Line']
        reordered_song_lines[new_index]['to_regenerate'] = row['Regenerate']
    st.session_state.song_lines = reordered_song_lines
    st.session_state.editor_content = "\n".join([line_data['current'] for line_data in reordered_song_lines.values()])

def display_generated_song():
    st.sidebar.write("### Biografia Espansa")
    st.sidebar.write(st.session_state.expanded_biography)
    st.sidebar.write("### Tema della canzone")
    st.sidebar.write(st.session_state.generated_themes)
    st.sidebar.write("### Descrizione Musicale")
    st.sidebar.write(st.session_state.music_description)
    st.sidebar.write("Vai qui e crea il brano: [Crea il brano](https://suno.com/create)")

    col1, col2 = st.columns([3, 2])

    with col1:
        col1x, col1empty, col1y = st.columns([1, 2, 1])

        with col1x:
            if st.button("Aggiungi Linea Vuota"):
                new_index = len(st.session_state.song_lines)
                st.session_state.song_lines[new_index] = {
                    "original": "",
                    "current": "",
                    "regeneration_count": 0,
                    "to_regenerate": False,
                    "to_be_green": False
                }
                st.session_state.editor_content = "\n".join([line_data['current'] for line_data in st.session_state.song_lines.values()])
                st.rerun()
        with col1y:
            if st.button("Rigenera Frasi"):
                regenerate_selected_lines()
                reset_checkboxes()
                st.rerun()
  
        # Prepare data for AG Grid
        song_lines = [{"Index": i, "Line": f"{line_data['current']}", "Regenerate": line_data['to_regenerate']} for i, line_data in st.session_state.song_lines.items()]
        df = pd.DataFrame(song_lines)

        # Configure AG Grid options
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

        # Accessing the data from grid_response correctly
        grid_data = pd.DataFrame(grid_response['data'])

        # Check if grid data has changed
        if not grid_data.equals(st.session_state.grid_data):
            st.session_state.grid_data = grid_data
            st.session_state.grid_changed = True
        else:
            st.session_state.grid_changed = False

        # Update session state with the edited lines
        update_session_state_from_grid(grid_data)

        if st.session_state.grid_changed:
            st.rerun()

    with col2:
        save_button = st.button("Save Lyrics")  # Button is defined first
        content = st_monaco(value=st.session_state.editor_content, height="1200px", language="plaintext", theme="vs-light")

        if save_button:  # Check if the save button is clicked
            st.session_state.editor_content = content
            updated_lines = content.split("\n")
            st.session_state.song_lines = {
                i: {"original": line, "current": line, "regeneration_count": 0, "to_regenerate": False, "to_be_green": False}
                for i, line in enumerate(updated_lines)
            }
            st.session_state.grid_data = pd.DataFrame([{"Index": i, "Line": line_data["current"], "Regenerate": line_data["to_regenerate"]}
                                                    for i, line_data in st.session_state.song_lines.items()])
            st.rerun()  # Rerun the app to reflect the changes

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

def main():
    initialize_session_state()
    
    if st.session_state.first_run:
        # Title and description
        st.title("Generatore di Canzoni")
        st.write("Inserisci una breve biografia del musicista e lascia che il nostro sistema crei una canzone personalizzata per te.")
        # Input fields and button in the main layout for the first run
        breve_biografia = st.text_area("Breve Biografia", value="Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo")
        tema = st.text_area("Tema", value="Cosa vuol dire essere ex trans, solo metafore stupide")
        generate_button = st.button("Genera Canzone")
        if generate_button:
            generate_song(breve_biografia, tema)
    else:
        # Input fields and button in the sidebar for subsequent runs
        with st.sidebar:
            st.success("Canzone generata con successo!")
            # Title and description
            st.title("Generatore di Canzoni")
            st.write("Inserisci una breve biografia del musicista e lascia che il nostro sistema crei una canzone personalizzata per te.")
            breve_biografia = st.text_area("Breve Biografia", value="Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo")
            tema = st.text_area("Tema", value="Cosa vuol dire essere ex trans, solo metafore stupide")
            generate_button = st.button("Genera Altra Canzone")
            if generate_button:
                generate_song(breve_biografia, tema)

    # Check if the song has been generated and display it
    if st.session_state.song_lines:
        display_generated_song()

if __name__ == "__main__":
    main()
