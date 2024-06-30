# utils.py

import os
import json
from config import USER_INPUT_PATH, EXPANDED_BIOGRAPFY_OUTPUT_PATH, GENERATED_THEMES_PATH, GENERATED_SONG_PATH, CORRECTED_SONG_PATH, MUSIC_DESCRIPTION_OUTPUT_PATH, SONG_EVALUATION_REPORT_PATH

def load_existing_files():
    def read_file(file_path):
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
    
    expanded_biography = read_file(EXPANDED_BIOGRAPFY_OUTPUT_PATH)
    generated_themes = read_file(GENERATED_THEMES_PATH)
    corrected_song_lines = read_file(CORRECTED_SONG_PATH).splitlines()
    music_description = read_file(MUSIC_DESCRIPTION_OUTPUT_PATH)
    try:
        user_input = json.load(open(USER_INPUT_PATH, 'r', encoding="utf-8"))
    except:
        user_input = "No user input found."
    
    print("Loaded expanded_biography: ", expanded_biography)
    print("Loaded generated_themes: ", generated_themes)
    print("Loaded corrected_song_lines: ", corrected_song_lines)
    print("Loaded music_description: ", music_description)
    print("Loaded user_input: ", user_input)
    
    return expanded_biography, generated_themes, corrected_song_lines, music_description, user_input

def check_existing_files():
    if all(os.path.exists(path) for path in [
        EXPANDED_BIOGRAPFY_OUTPUT_PATH,
        GENERATED_THEMES_PATH,
        CORRECTED_SONG_PATH,
        MUSIC_DESCRIPTION_OUTPUT_PATH,
        #USER_INPUT_PATH,
        
    ]):
        return True
    return False

def flush_existing_files():
    for path in [
        EXPANDED_BIOGRAPFY_OUTPUT_PATH,
        GENERATED_THEMES_PATH,
        CORRECTED_SONG_PATH,
        MUSIC_DESCRIPTION_OUTPUT_PATH,
        USER_INPUT_PATH,
        SONG_EVALUATION_REPORT_PATH,
        GENERATED_SONG_PATH
    ]:
        if os.path.exists(path):
            os.remove(path)
            
def save_expanded_biography(expanded_biography):
    with open(EXPANDED_BIOGRAPFY_OUTPUT_PATH, 'w', encoding="utf-8") as file:
        file.write(expanded_biography)

def save_generated_themes(generated_themes):
    with open(GENERATED_THEMES_PATH, 'w', encoding="utf-8") as file:
        file.write(generated_themes)

def save_corrected_song_lines(corrected_song_lines):
    with open(CORRECTED_SONG_PATH, 'w', encoding="utf-8") as file:
        file.write("\n".join(corrected_song_lines))

def save_music_description(music_description):
    with open(MUSIC_DESCRIPTION_OUTPUT_PATH, 'w', encoding="utf-8") as file:
        file.write(music_description)
        
def save_user_input(breve_biografia, tema):
    user_input = {
        "breve_biografia": breve_biografia,
        "tema": tema
    }
    os.makedirs(os.path.dirname(USER_INPUT_PATH), exist_ok=True)
    with open(USER_INPUT_PATH, 'w', encoding="utf-8") as file:
        json.dump(user_input, file)