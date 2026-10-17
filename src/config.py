import os
from google import genai
from google.genai import types
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
EMBED_MODEL = "gemini-embedding-2"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

_client = None  # created once, then reused


def configuration():
    global _client
    if _client is not None:
        return _client

    if not API_KEY:
        print("GEMINI_API_KEY is missing. Add it to your .env file.")
        return None

    try:
        _client = genai.Client(api_key=API_KEY)
        return _client
    except Exception as e:
        print(f"Error initializing the Gemini client: {e}")
        return None
    
def get_model_config(system_instruction:str):
    config= types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
    return config
