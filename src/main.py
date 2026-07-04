import sys
import config
import prompts
import utils
import chatbot

def main():
    client = config.configuration()

    if client is None:
        print("Failed to initialize the Gemini client. Exiting the program.")
        sys.exit(1)

    utils.display_personas(prompts.PERSONAS)
    choice = utils.get_valid_input("Enter the number corresponding to your choice of persona: ")

    selected_instruction = prompts.get_persona(choice)

    chatbot.start_chat_session(client, selected_instruction)

if __name__ == "__main__":
    main()