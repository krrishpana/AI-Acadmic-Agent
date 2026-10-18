from google import genai
import os
import config
import vector_store
import embedding_engine
import query_engine

from langchain_core.tools import tool

collection = vector_store.get_vector_collection()

@tool
def search_notes(query: str) -> str:
    """
    Searches the persistent vector database for specific concepts, facts, or context 
    matching the user's academic query. Returns the top 3 relevant context blocks.
    """
    # client = config.configuration()

    # if not client:
    #     return "Error: Gemini client is not initialized."
    
    try:
        results = query_engine.retrieve(query, top_k=4)

        if not results:
            return "No relevant context found for the given query."

        context_chunks = []
        sources_used = set()

        for item in results:
            context_chunks.append(item["text"])
            meta = item["metadata"]
            source_file = meta.get("source", "Unknown PDF")
            page_num = meta.get("page", "?")
            sources_used.add(f"{source_file} (Page {page_num})")

        context_text = "\n---\n".join(context_chunks)
        sources_text = "\n".join(f"- {s}" for s in sorted(sources_used))

        return f"Retrieved Notes:\n{context_text}\n\nSources Used:\n{sources_text}"

    except Exception as e:
        print(f"Error during search: {e}")
        return f"Error executing search: {e}"


@tool
def summarize_notes(filename: str) -> str:
    """
    Summarizes ONE whole document from the student's notes.
    'filename' must be the document's file name, e.g. 'ai_notes.pdf'.
    If you are not sure of the exact name, call list_documents first.
    """
    # CHANGED: the docstring above (see change 1)

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    try:
        # NEW: find the real file name, ignoring upper/lower case
        sources = vector_store.get_all_sources(collection)

        wanted = filename.strip().lower()
        if not wanted.endswith(".pdf"):
            wanted += ".pdf"

        match = None
        for source in sources:
            if source.lower() == wanted:
                match = source
                break

        # NEW: if nothing matches, tell the LLM the real names
        if match is None:
            return (
                f"No document named '{filename}'. "
                f"Available documents: {', '.join(sources)}. "
                f"Call summarize_notes again with one of these exact names."
            )

        # CHANGED: search with `match` (the real name), not `filename`
        records = collection.get(where={"source": match})
        document = records.get('documents', [])

        if not document:
            return f"No documents found for the file: {match}"
        
        full_text = " ".join(document)[:8000]

        prompt = f"Provide a comprehensive, high-level summary of the following document content:\n\n{full_text}"
        response = client.models.generate_content(
            model=config.MODEL,
            contents=prompt
        )

        return response.text
    except Exception as e:
        print(f"An error occurred while summarizing the notes.: {e}")
        return f"Error summarizing notes: {e}"


@tool   
def create_quiz(topic: str)-> str:
    """
    Generates a 3-question conceptual quiz (with multiple choice or short answers) based 
    on a specific academic topic to test the user's understanding.
    """

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    context = search_notes.func(topic)

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
        return f"Error generating quiz: {e}"


@tool
def generate_flashcards(topic: str) -> str:
    """
    Generates a set of high-impact Front/Back flashcards for active recall study sessions.
    """

    client = config.configuration()

    if not client:
        return "Error: Gemini client is not initialized."
    
    context = search_notes.func(topic)

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
        return f"Error generating flashcards {e}"


@tool
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
        return f"Error making study plan {e}"
    
@tool
def list_documents() -> str:
    """
    Lists the file names of all documents in the student's notes database.
    Use this when the user asks what notes are available, or before
    summarize_notes if you are unsure of the exact file name.
    """
    sources = vector_store.get_all_sources(collection)
    if not sources:
        return "No documents have been indexed yet."
    return "Available documents:\n" + "\n".join(f"- {s}" for s in sources)

all_tools = [
    search_notes,
    summarize_notes,
    create_quiz,
    generate_flashcards,
    study_plan,
    list_documents
]