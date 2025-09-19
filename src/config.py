import logging
from pathlib import Path

from dotenv import load_dotenv
import os

load_dotenv()

SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent

# Use correct SQLite URL format (three slashes for absolute paths)
DATABASE_URL = f"sqlite:///{ROOT_DIR / 'database.sqlite'}"

# Logging configuration
LOG_FILE = ROOT_DIR / "pakytarefas.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

MEDIA_DIR = ROOT_DIR / "media"

MEDIA_DIR.mkdir(exist_ok=True)

WUZAPI_SERVER_URL = os.environ["WUZAPI_SERVER_URL"]
WUZAPI_TOKEN = os.environ["WUZAPI_TOKEN"]
