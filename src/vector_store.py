import chromadb 
import document_loader

def get_vector_collection(db_path: str = "./chroma_db", collection: str = "ai_notes"):
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_or_create_collection(name="my_collection")

    return collection

def add_to_vector_store(collection, ids: list[str], documents: list[str], embeddings: list[list[float]]) -> None:

    try:
        collection.add(
        documents= documents,
        embeddings= embeddings,
        ids= ids)
        print(f"Successfully indexed {len(documents)} chunks into the vector store.")

    except Exception as e:
        print(f"Error adding to vector store: {e}")
