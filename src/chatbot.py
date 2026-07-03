import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

HISTORY_FILE = "chat_history.json"

PERSONAS = {
    "1": "You are a university professor who explains things with academic rigor. Always provide detailed explanations and cite sources when possible.",
    "2": "You are a strict technical interviewer who evaluates code efficiency and correctness. Always ask follow-up questions to probe deeper into the candidate's understanding.",
    "3": "You are a Socratic AI mentor who never gives direct answers but asks guiding questions to help the user arrive at their own conclusions. Always encourage critical thinking and exploration."
}

def get_valid_input(prompt):
    while True:
        user_input = input(prompt)
        if user_input.strip() != "":
            return user_input
        print("Input cannot be empty. Please try again.")

def main():
    api_from_env = os.getenv("GEMINI_API_KEY")

    try:
        client = genai.Client(api_key=api_from_env)

        #testing the client initialization by making a simple call to the model
        client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Ping"
        )                       

    except Exception as e:
        print("Error initializing the Gemini client. Please check your API key and environment variables.")
        print(f"Exception details: {e}")
        return

    print("Select a persona for the chatbot:")
    for key, description in PERSONAS.items():
        print(f"{key}: {description}")

    choice = input("Enter the number corresponding to your choice: ")
    selected_system_instruction = PERSONAS.get(choice, PERSONAS["1"])  

    config= types.GenerateContentConfig(
                system_instruction=selected_system_instruction,
                temperature=0.7,
            )

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            save_dicts= json.load(f)
            history = [types.Content(**item) for item in save_dicts]

    else:
        history = []

    userinput = get_valid_input("User: ")

    while userinput.lower() != 'end':
        history.append(types.Content(
            role= "user",
            parts= [types.Part.from_text(text = userinput)]
        ))

        try:
            print("Statbot: Thinking...", end="", flush=True)
            systemoutput = client.models.generate_content_stream(
                contents= history,
                model = "gemini-2.5-flash-lite",
                config= config
            )
        except Exception as e:
            print("Error generating content from the Gemini model. Please check your network connection and model availability.")
            break

        full_response = ""

        first_chunk = True

        try:
            for chunk in systemoutput:
                if first_chunk:
                    print("\rStatbot: ", end="", flush=True)
                    first_chunk = False
                print(chunk.text, end="", flush=True)
                full_response += chunk.text
        except Exception as e:
            print("\nError while streaming the response. Please try again.")
            print(f"Exception details: {e}")

            print()

        history.append(types.Content(
                role= "model",
                parts= [types.Part.from_text(text = full_response)]
            ))

        userinput = get_valid_input("User: ")
        

    with open(HISTORY_FILE, 'w') as f:
        json_ready_history = [message.model_dump() for message in history]
        json.dump(json_ready_history, f, indent=4)

if __name__ == "__main__":
    main()

