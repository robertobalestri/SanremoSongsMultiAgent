import os

# Define a variable to check if we are running locally or in the cloud
IS_LOCAL = os.path.exists(".env")
if not IS_LOCAL:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Define the paths to the input and output files
BASE_EXTRACTED_DIR = 'data/extracted'
EXPANDED_BIOGRAPFY_OUTPUT_PATH = f'data/extracted/expanded_musician_biography.txt'
GENERATED_THEMES_PATH = f'data/extracted/generated_themes.txt'
GENERATED_SONG_PATH = f'data/extracted/generated_song.txt'
SONG_EVALUATION_REPORT_PATH = f'data/extracted/song_evaluation_report.txt'
CORRECTED_SONG_PATH = f'data/extracted/corrected_song.txt'
MUSIC_DESCRIPTION_OUTPUT_PATH = f'data/extracted/music_description.txt'
USER_INPUT_PATH = f'data/extracted/user_input.json'
DATABASE_ZIP_CANZONI_DIR = f'data/db_songs/'

DEFAULT_SONG_NAME = "default_song"