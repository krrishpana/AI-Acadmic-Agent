import os
import json
from google.genai import types
import base64

HISTORY_FILE = "chat_history.json"

def clean_bytes(obj):
    """Recursively converts bytes objects to Base64 strings for JSON serialization."""
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, dict):
        return {k: clean_bytes(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_bytes(item) for item in obj]
    return obj

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                save_dicts= json.load(f)
                return [types.Content.model_validate(item) for item in save_dicts]
        except(json.JSONDecodeError, TypeError) as e:
            print(f"Error loading history: {e}. Starting with an empty history.")
            return []
    else:
        history = []

    return history

def save_history(history):
    try:
        json_ready_history = []
        for message in history:
            message_dict = message.model_dump()
            cleaned_message = clean_bytes(message_dict)
            json_ready_history.append(cleaned_message)

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json_ready_history = [message.model_dump() for message in history]
            json.dump(json_ready_history, f, indent=4)
    except Exception as e:
        print(f"Error saving history: {e}.")