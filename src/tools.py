from google import genai
import os
import config
import vector_store

collection = vector_store.get_vectore_collection()

def search_notes(query: str) -> str:
    """
    Searches the persistent vector database for specific concepts, facts, or context 
    matching the user's academic query. Returns the top 3 relevant context blocks.
    """
    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    try:
    
        response = client.model.embed_content(
            model=config.EMBED_MODEL,
            contents=query
        )

        query_vector = response.embeddings[0].values

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=3,
        )

        documents = results.get('documents', [[]])[0]

        if not documents:
            return "No relevant context found for the given query."
        
        return "\n---\n".join(documents)

    except Exception as e:
        print(f"Error during search: {e}")


def summarize_notes(filename: str) -> str:
    """
    summarizes the relevant context blocks retrieved from the vector database based on the user's query.
    """
    client = config.configuration()

    if not config:
        return "Error: Gemini client is not initialized."
    
    try:
        records = collection.get(where={"source": filename})
        document = records.get('documents', [])

        if not document:
            return f"No documents found for the file: {filename}"
        
        full_text = " ".join(document)[:8000]

        prompt = f"Provide a comprehensive, high-level summary of the following document content:\n\n{full_text}"
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt
        )

        return response.text
    except Exception as e:
        print(f"An error occurred while summarizing the notes.: {e}")
    
def create_quiz(topic: str)-> str:
    """
    Generates a 3-question conceptual quiz (with multiple choice or short answers) based 
    on a specific academic topic to test the user's understanding.
    """

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    context = search_notes(topic)

    prompt = f"""
    Based on the following academic reference material:
    {context}
    
    Generate a challenging 3-question conceptual quiz on the topic: '{topic}'.
    Include Multiple Choice layout for each question and clearly hide the correct answers at the very bottom.
    """

    try:
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt
        )

        return response.text
    except Exception as e:
        print(f"An error occurred while generating the quiz: {e}")

def generate_flashcards(topic: str) -> str:
    """
    Generates a set of high-impact Front/Back flashcards for active recall study sessions.
    """

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    context = search_notes(topic)

    prompt = f"""
    Based on the following academic reference material:
    {context}
    
    Generate a set of high-impact Front/Back flashcards for active recall study sessions on the topic: '{topic}'.
    Ensure that each flashcard has a clear question on the front and a concise answer on the back.
    """

    try:
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt
        )

        return response.text
    except Exception as e:
        print(f"An error occurred while generating flashcards: {e}")


def study_plan(objective: str) -> str:
    """
    Generates a structured, chronological daily study roadmap based on a target academic deadline 
    or exam objective provided by the user.
    """

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    prompt = f"""
    Create a structured, chronological daily study roadmap based on the following target academic deadline or exam objective:
    {objective}
    
    Ensure that the study plan is realistic, actionable, and tailored to the user's learning pace.
    """

    try:
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt
        )

        return response.text
    except Exception as e:
        print(f"An error occurred while generating the study plan: {e}")
