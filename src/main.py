import sys
import config
import prompts
import utils
import chatbot

import document_loader
import text_splitter
import embedding_engine
import vector_store
import query_engine

def run_rag_pipeline():
    print("Starting the RAG pipeline...")

    client = config.configuration()

    if client is None:
        print("Failed to initialize the Gemini client. Exiting the program.")
        sys.exit(1)

    collection = vector_store.get_vector_collection()

    pdf_path = "/Users/krrishpanakarmacharya/Desktop/Projects/data/ai_notes.pdf" 
    print(f"\n Scanning for knowledge source: '{pdf_path}'...")

    try:
        raw_text = document_loader.load_pdf(pdf_path)

        if raw_text:
            chunks = text_splitter.split_text(raw_text, chunk_size=500, chunk_overlap=50)
            print(f"Fragmented document into {len(chunks)} individual semantic blocks.")

        embeddings=[]
        ids =[]

        for i, chunk in enumerate(chunks):
            vector = embedding_engine.get_embedding(client, chunk)
            if vector:
                embeddings.append(vector)
                ids.append(f"doc_chunk_{i}")

        if embeddings:
                vector_store.add_to_vector_store(collection, ids, chunks, embeddings)
                
    except Exception as e:
        print(f" Ingestion skipped or failed: {e}. Attempting to use existing database cache.")

    utils.display_personas(prompts.PERSONAS)
    choice = utils.get_valid_input("Enter the number corresponding to your choice of persona: ")

    selected_instruction = prompts.get_persona(choice)

    chatbot.start_chat_session(client, selected_instruction, collection)

if __name__ == "__main__":
    run_rag_pipeline()