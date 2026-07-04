def get_valid_input(prompt: str) -> str:
    while True:
        user_input = input(prompt)
        if user_input.strip() != "":
            return user_input
        print("Input cannot be empty. Please try again.")

def display_personas(PERSONAS: dict):
    print("Select a persona for the chatbot:")
    for key, description in PERSONAS.items():
        print(f"{key}: {description}")
 
