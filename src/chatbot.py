from google.genai import types
import config
from history import load_history, save_history
from prompts import PERSONAS
from utils import get_valid_input

def start_chat_session(client, system_instruction: str):
    history = load_history()

    model_config = config.get_model_config(system_instruction)

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
                config= model_config
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

    save_history(history)


