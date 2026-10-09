import sys
import glob
import os

import config
import prompts
import utils
import document_loader
import text_splitter
import embedding_engine
import vector_store
from graph_agent import rag_agent
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


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

            embeddings = []
            ids = []
            documents = []
            metadatas = []

            for record in chunk_records:
                chunk_text = record["text"]
                chunk_meta = record["metadata"]
                chunk_meta["source"] = filename

                vector = embedding_engine.get_embedding(client, chunk_text)
                if vector:
                    embeddings.append(vector)
                    documents.append(chunk_text)
                    metadatas.append(chunk_meta)
                    ids.append(f"{filename}_chunk_{global_chunk_count}")
                    global_chunk_count += 1

            if embeddings:
                vector_store.add_to_vector_store(collection, ids, documents, embeddings, metadatas)
                print(f" Successfully indexed '{filename}' with metadata into vector database.")
                
        except Exception as e:
            print(f"  Failed to process '{filename}': {e}")

    print(f"\n Ingestion complete! Total items stacked in database: {global_chunk_count}")
    print("-------------------------------------------------------------------\n")

    # Persona Selection
    utils.display_personas(prompts.PERSONAS)
    choice = utils.get_valid_input("Enter the number corresponding to your choice of persona: ")
    selected_instruction = prompts.get_persona(choice)

    # Agent Instruction Setup
    agent_instruction = f"""
    {selected_instruction}

    You are an AI Academic Agent. You have access to specialized tools:
    - search_notes: Searches the student's vector store notes for specific information.
    - summarize_notes: Summarizes relevant context blocks from the vector database.
    - create_quiz: Generates conceptual quizzes on topics.
    - generate_flashcards: Generates active recall flashcards.
    - study_plan: Creates structured study schedules.

    Use your tools whenever appropriate to fulfill the user's intent.

    CRITICAL CITATION RULE:
    Whenever you use the 'search_notes' tool to answer a question, you MUST include a "Sources:" section at the very end of your response, listing the exact PDF filenames and page numbers provided in the tool output.
    """

    print("\n AI Academic Agent ready! (Type 'end' to save and exit)\n")
    
    thread_config = {
        "configurable": {"thread_id": "default_session"},
        "recursion_limit": 10,
    }

    # Single Execution Loop
    while True:
        userinput = utils.get_valid_input("User: ")
        
        if userinput.lower() == 'end':
            break

        try:
            print("AI Agent: Thinking...", end="", flush=True)
            
            response = rag_agent.invoke(
                {
                    "messages": [HumanMessage(content=userinput)],
                    "system_prompt": agent_instruction,
                },
                config=thread_config
            )
            
            ai_message = response["messages"][-1]
            
            print(f"\r\033[KAI Agent: {ai_message.text}\n")

        except Exception as e:
            print(f"\n\r\033[K[Error during conversation]: {e}\n")
            break

    print("\nSession ended. Goodbye!")

if __name__ == "__main__":
    run_rag_pipeline()