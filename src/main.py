import uuid

import prompts
import utils
import agent_service


def run_cli():
    utils.display_personas(prompts.PERSONAS)
    persona = utils.get_valid_input("Enter the number of your persona: ")
    thread_id = str(uuid.uuid4())  # a new conversation every run

    print("\nAI Academic Agent ready! (Type 'end' to exit)\n")

    while True:
        user_input = utils.get_valid_input("User: ")
        if user_input.lower() == "end":
            break

        try:
            result = agent_service.chat(user_input, thread_id, persona)
            if result["tools_used"]:
                print(f"[tools used: {', '.join(result['tools_used'])}]")
            print(f"AI Agent: {result['answer']}\n")
        except Exception as e:
            print(f"[Error]: {e}\n")

    print("Session ended. Goodbye!")


if __name__ == "__main__":
    run_cli()