import os

# Define a variable to check if we are running locally or in the cloud
IS_LOCAL = os.path.exists(".env")
if not IS_LOCAL:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Define the paths to the input and output files
EXPANDED_BIOGRAPFY_OUTPUT_PATH = f'data/output/expanded_musician_biography.txt'
GENERATED_THEMES_PATH = f'data/output/generated_themes.txt'
GENERATED_SONG_PATH = f'data/output/generated_song.txt'
SONG_EVALUATION_REPORT_PATH = f'data/output/song_evaluation_report.txt'
CORRECTED_SONG_PATH = f'data/output/corrected_song.txt'
MUSIC_DESCRIPTION_OUTPUT_PATH = f'data/output/music_description.txt'