import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

HISTORY_FILE = "chat_history.json"

def main():
    api_from_env = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_from_env)

    print("Chat starts here... type 'end' to end the conversation.")

    
    userinput = input("User: ")

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            save_dicts= json.load(f)
            history = [types.Content(**item) for item in save_dicts]

    else:
        history = []

    while userinput.lower() != 'end':
        history.append(types.Content(
            role= "user",
            parts= [types.Part.from_text(text = userinput)]
        ))
        systemoutput = client.models.generate_content(
            contents= history,
            model = "gemini-2.5-flash-lite",
            config= types.GenerateContentConfig(
                system_instruction="Answer in 1 line , within 50 characters.",
                temperature=0.5,
            )
        )

        history.append(types.Content(
            role= "model",
            parts =[types.Part.from_text(text = systemoutput.text)]
        ))

        print("Statbot : ", systemoutput.text)
        userinput = input("User: ")

    with open(HISTORY_FILE, 'w') as f:
        json_ready_history = [message.model_dump() for message in history]
        json.dump(json_ready_history, f, indent=4)

if __name__ == "__main__":
    main()

