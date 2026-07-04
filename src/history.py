import os
import json
from google.genai import types

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                save_dicts= json.load(f)
                history = [types.Content(**item) for item in save_dicts]
        except(json.JSONDecodeError, TypeError) as e:
            print(f"Error loading history: {e}. Starting with an empty history.")
            return []
    else:
        history = []

    return history

def save_history(history):
    try:
        with open(HISTORY_FILE, 'w') as f:
            json_ready_history = [message.model_dump() for message in history]
            json.dump(json_ready_history, f, indent=4)
    except Exception as e:
        print(f"Error saving history: {e}.")