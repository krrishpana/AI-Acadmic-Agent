import glob
import os

import config
import document_loader
import text_splitter
import embedding_engine
import vector_store


def ingest_documents():
    client = config.configuration()
    if client is None:
        print("Gemini client not available. Stopping.")
        return

    collection = vector_store.get_vector_collection()
    pdf_files = glob.glob(os.path.join(config.DATA_DIR, "*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in '{config.DATA_DIR}'.")
        return

    print(f"Found {len(pdf_files)} PDF(s).")
    total_chunks = 0

    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)

        if vector_store.file_exists_in_store(collection, filename):
            print(f"'{filename}' already indexed. Skipping.")
            continue

        print(f"Processing '{filename}'...")
        try:
            docs_with_metadata = document_loader.load_pdf(pdf_path)
            if not docs_with_metadata:
                print(f"No text found in '{filename}'. Skipping.")
                continue

            chunk_records = text_splitter.split_text(docs_with_metadata)

            ids, documents, embeddings, metadatas = [], [], [], []
            for i, record in enumerate(chunk_records):
                vector = embedding_engine.get_embedding(client, record["text"])
                if vector:
                    meta = record["metadata"]
                    meta["source"] = filename
                    ids.append(f"{filename}_chunk_{i}")
                    documents.append(record["text"])
                    embeddings.append(vector)
                    metadatas.append(meta)

            if embeddings:
                vector_store.add_to_vector_store(collection, ids, documents, embeddings, metadatas)
                total_chunks += len(embeddings)

        except Exception as e:
            print(f"Failed to process '{filename}': {e}")

    print(f"Ingestion complete. New chunks added: {total_chunks}")


if __name__ == "__main__":
    ingest_documents()