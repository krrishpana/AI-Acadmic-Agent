import sys
import config
import prompts
import utils
import chatbot
import glob
import os

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

    data_directory = "/Users/krrishpanakarmacharya/Desktop/Projects/data"
    pdf_files = glob.glob(os.path.join(data_directory, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{data_directory}'. Please check your path.")
        sys.exit(1)

    print(f"\n Scanning directory... Found {len(pdf_files)} knowledge source(s).")

    global_chunk_count = 0

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)
        print(f"\n Processing knowledge source: '{filename}'...")

        try:
            raw_text = document_loader.load_pdf(pdf_path)

            if raw_text:
                chunks = text_splitter.split_text(raw_text)
                print(f"Fragmented {filename} into {len(chunks)} individual semantic blocks.")

            embeddings=[]
            ids =[]

            for i, chunk in enumerate(chunks):
                vector = embedding_engine.get_embedding(client, chunk)
                if vector:
                    embeddings.append(vector)
                    ids.append(f"{filename}_chunk_{global_chunk_count}")
                    global_chunk_count += 1

            if embeddings:
                    vector_store.add_to_vector_store(collection, ids, chunks, embeddings)
                    
        except Exception as e:
            print(f"  Failed to process '{filename}': {e}")

    print(f"\n Ingestion complete! Total items stacked in database: {global_chunk_count}")
    print("-------------------------------------------------------------------\n")

    utils.display_personas(prompts.PERSONAS)
    choice = utils.get_valid_input("Enter the number corresponding to your choice of persona: ")

    selected_instruction = prompts.get_persona(choice)

    chatbot.start_chat_session(client, selected_instruction, collection)

if __name__ == "__main__":
    run_rag_pipeline()