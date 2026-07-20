from google.genai import types
import config
from history import load_history, save_history
from prompts import PERSONAS
from utils import get_valid_input
import embedding_engine
import query_engine
import tools

def start_chat_session(client, system_instruction: str, collection):
    history = load_history()

    agent_instruction = f"""
    {system_instruction}

    You are an AI Academic Agent. You have access to specialized tools:
    - search_notes: Searches the student's vector store notes for specific information.
    - summarize_notes: Summarizes relevant context blocks from the vector database.
    - create_quiz: Generates conceptual quizzes on topics.
    - create_flashcards: Generates active recall flashcards.
    - study_plan: Creates structured study schedules.

    Use your tools whenever appropriate to fulfill the user's intent.
    """

    agent_config = types.GenerateContentConfig(
        system_instruction=agent_instruction,
        tools=[tools.search_notes, tools.summarize_notes ,tools.create_quiz, tools.generate_flashcards, tools.study_plan],
        temperature=0.2
    )

    chat = client.chats.create(
        model=config.MODEL,
        config=agent_config,
        history=history
    )

    print("\n Statbot is ready! (Type 'end' to save and exit)\n")
    userinput = get_valid_input("User: ")

    while userinput.lower() != 'end': 

        try:
            print("Statbot: Thinking...", end="", flush=True)
            response = chat.send_message(userinput)

            print("\r\033[KStatbot: ", end="", flush=True)
            print(response.text)
            print()

        except Exception as e:
            print(f"\n\r\033[K[Error during conversation]: {e}\n")
            break

        userinput = get_valid_input("\nUser: ")

    save_history(chat.get_history())


