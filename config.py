import os
from dotenv import load_dotenv
load_dotenv()

# Define a variable to check if we are running locally or in the cloud
IS_LOCAL = os.path.exists(".env")
if not IS_LOCAL:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
    
PASSWORD = os.getenv("PASSWORD")

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

DEFAULT_BREVE_BIO = "Ragazza dall'anima latina, ex trans (è ritornata al proprio sesso originale di nascita), fa goth k pop con influenze bossanova. Nata come Manuela, oggi si chiama Manuela, ma fu Manuel Caproni durante quei 13 mesi da uomo. E' la prima baritono donna del mondo."
DEFAULT_TEMA_CANZONE = "Cosa vuol dire essere ex trans, usando solo metafore stupide, non intellettuale, deve essere un pezzo becero."