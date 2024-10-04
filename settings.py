import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')

API_URL = 'http://127.0.0.1:8000/api/v1'

BASE_DIR = Path(__file__).resolve().parent
