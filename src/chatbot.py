from google.genai import types
import config
from history import load_history, save_history
from prompts import PERSONAS
from utils import get_valid_input
import embedding_engine
import query_engine

def start_chat_session(client, system_instruction: str, collection):
    history = load_history()

    model_config = config.get_model_config(system_instruction)

    userinput = get_valid_input("User: ")

    while userinput.lower() != 'end':

        try:
            print("\n Searching local PDF database for answers...")
            
            query_vector = embedding_engine.get_embedding(client, userinput)
        
            retrieved_chunks = query_engine.search_database(collection, query_vector, top_k=3)
            
            context_block = "\n---\n".join(retrieved_chunks)

            augmented_prompt = f"""[CONTEXT FROM LOCAL NOTES]:
{context_block}

[USER QUESTION]:
{userinput}

[INSTRUCTION]:
Answer the user question using the context data provided above. If the context does not fully cover the answer, use your general knowledge to fill in the gaps, but prioritize and ground your explanation in any relevant terms mentioned in the context snippets."""

            userinput = augmented_prompt

        except Exception as e:
            print(f"RAG Retrieval failed ({e}). Proceeding with standard fallback memory...")
        history.append(types.Content(
            role= "user",
            parts= [types.Part.from_text(text = userinput)]
                ))

        try:
            print("Statbot: Thinking...", end="", flush=True)
            systemoutput = client.models.generate_content_stream(
                contents= history,
                model = "gemini-2.5-flash",
                config= model_config
            )
        except Exception as e:
            print("Error generating content from the Gemini model. Please check your network connection and model availability.")
            break

        full_response = ""

        first_chunk = True

        try:
            for chunk in systemoutput:
                if chunk and chunk.text:
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


