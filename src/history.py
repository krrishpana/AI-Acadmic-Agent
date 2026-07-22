# history.py
import os
import json
import base64
from google.genai import types

HISTORY_FILE = "chat_history.json"

def sanitize_for_json(obj):
    """
    Recursively converts any bytes/binary payloads (like thought_signatures 
    or internal tool tokens) into plain text Base64 strings.
    """
    if isinstance(obj, bytes):
        return base64.b64encode(obj).decode('utf-8')
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_json(item) for item in obj]
    elif isinstance(obj, tuple):
        return [sanitize_for_json(item) for item in obj]
    return obj

def load_history():
    """Loads saved JSON history back into SDK Content objects."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            saved_dicts = json.load(f)
            return [types.Content.model_validate(item) for item in saved_dicts]
    except Exception as e:
        print(f"Notice: Couldn't parse existing chat history ({e}). Starting fresh.")
        return []

def save_history(history):
    """Sanitizes binary data and persists chat history to disk."""
    try:
        json_ready_history = []
        for message in history:
            raw_dict = message.model_dump()
            clean_dict = sanitize_for_json(raw_dict)
            json_ready_history.append(clean_dict)

        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(json_ready_history, f, indent=4)
            
        print("\nChat history saved successfully!")

    except Exception as e:
        print(f"\nError saving history: {e}")