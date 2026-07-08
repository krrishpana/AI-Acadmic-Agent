from google.genai import types

def get_embedding(client, text_to_embed: str) -> list[float]:

    if not text_to_embed.strip():
        print("Warning: The input text is empty or whitespace. Returning an empty embedding.")
        return []
    
    EMBED_MODEL = "gemini-embedding-2"

    try:
        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents= text_to_embed
        )

        if response and response.embeddings:
            vector = response.embeddings[0].values
            return vector
        
        return []
    
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
