import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
EMBED_MODEL = "gemini-embedding-001"

def configuration():
    try:
        client = genai.Client(api_key=API_KEY)

        #testing the client initialization by making a simple call to the model
        client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Ping"
        ) 
        return client                      

    except Exception as e:
        print("Error initializing the Gemini client. Please check your API key and environment variables.")
        print(f"Exception details: {e}")
        return None
    
def get_model_config(system_instruction:str):
    config= types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
    return config
