from google import genai
from google.genai import types
from dotenv import load_load_env

load_env()

def main():
    client = genai.Client()

    print("Chat starts here... type 'end' to end the conversation.")

    userinput = input("User: ")

    while userinput.lower() != 'end':
        systemoutput = client.models.generate_content(
            contents= userinput,
            model = "gemini-2.5-flash-lite",
            config= types.GenerateContentConfig(
                system_instruction="Answer in 1 line , within 50 characters.",
                temperature=0.5,
            )
        )

        print("Statbot : ", systemoutput.text)
        userinput = input("User: ")

if __name__ == "__main__":
    main()

