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

        if vector_store.file_exists_in_store(collection, filename):
            print(f" '{filename}' is already indexed in the vector store. Skipping ingestion.")
            continue

        print(f"\n Processing knowledge source: '{filename}'...")

        try:
            docs_with_metadata = document_loader.load_pdf(pdf_path)

            if docs_with_metadata:
                chunk_records = text_splitter.split_text(docs_with_metadata)
                print(f"Fragmented {filename} into {len(chunk_records)} individual semantic blocks.")

            embeddings=[]
            ids =[]
            documents = []
            metadatas = []

            for record in chunk_records:
                    chunk_text = record["text"]
                    chunk_meta = record["metadata"]

                    vector = embedding_engine.get_embedding(client, chunk_text)
                    if vector:
                        embeddings.append(vector)
                        documents.append(chunk_text)
                        metadatas.append(chunk_meta)
                        
                        # Combines filename and global count for an elite, non-colliding ID string
                        ids.append(f"{filename}_chunk_{global_chunk_count}")
                        global_chunk_count += 1

            if embeddings:
                # Pass the metadata list straight to your updated vector store function!
                vector_store.add_to_vector_store(collection, ids, documents, embeddings, metadatas)
                print(f" Successfully indexed '{filename}' with metadata into vector database.")
                
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