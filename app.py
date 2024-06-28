import streamlit as st
from crew.crew import main_crew

# Title and description
st.title("Generatore di Canzoni")
st.write("Inserisci una breve biografia del musicista e lascia che il nostro sistema crei una canzone personalizzata per te.")

# Input field for the brief biography
breve_biografia = st.text_area("Breve Biografia", value="Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo")

# Button to start the process
if st.button("Genera Canzone"):
    # Display a loading message
    with st.spinner("Generazione della canzone in corso..."):
        # Get your crew to work!
        result = main_crew.kickoff(inputs={"topic": breve_biografia})
        
        
        # Read the output files
        expanded_biography_output_path = f'data/output/expanded_musician_biography.txt'
        generated_themes_path = f'data/output/generated_themes.txt'
        generated_song_path = f'data/output/generated_song.txt'
        song_evaluation_report_path = f'data/output/song_evaluation_report.txt'
        corrected_song_path = f'data/output/corrected_song.txt'
        music_description_output_path = f'data/output/music_description.txt'
        
        with open(expanded_biography_output_path, 'r', encoding= "utf-8") as file:
            expanded_biography = file.readlines()
        
        with open(corrected_song_path, 'r', encoding= "utf-8") as file:
            corrected_song = file.readlines()
        
        with open(music_description_output_path, 'r', encoding= "utf-8") as file:
            music_description = file.readlines()
        
        expanded_biography = '\n'.join(expanded_biography)
        corrected_song = '\n'.join(corrected_song)
        music_description = '\n'.join(music_description)

    # Display the results
    st.success("Canzone generata con successo!")
    st.write("### Biografia Espansa")
    st.write(expanded_biography)
    st.write("### Canzone Corretta")
    st.write(corrected_song)
    st.write("### Descrizione Musicale")
    st.write(music_description)

# Display usage metrics
st.write("### Metriche di Utilizzo")
st.write(main_crew.usage_metrics)