from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

STORAGE_DIRECTORY_NAME = 'Reflections'

STORAGE_DIRECTORY = BASE_DIR / (STORAGE_DIRECTORY_NAME if not DEBUG else 'Test Storage')
STORAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)