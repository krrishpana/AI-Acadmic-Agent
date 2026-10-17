import chromadb 
import document_loader
import config

def get_vector_collection(collection_name: str = "my_collection"):
    chroma_client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    return chroma_client.get_or_create_collection(name=collection_name)

def add_to_vector_store(collection, ids: list[str], documents: list[str], embeddings: list[list[float]], metadata: list[dict]) -> None:

    try:
        collection.add(
        documents= documents,
        embeddings= embeddings,
        ids= ids,
        metadatas= metadata)
        print(f"Successfully indexed {len(documents)} chunks into the vector store.")

    except Exception as e:
        print(f"Error adding to vector store: {e}")

def file_exists_in_store(collection, file_name: str) -> bool:
    try:
        # Check if any document in the collection has the given file_name in its metadata
        existing = collection.get(
            where={"source": file_name},
            limit = 1
        )
        return len(existing.get('ids', [])) > 0
    except Exception as e:
        print(f"Error checking file existence in vector store: {e}")
        return False
    
def get_all_sources(collection) -> list[str]:
    result = collection.get(include=["metadatas"])
    return sorted({
        metadata["source"]
        for metadata in result["metadatas"]
        if metadata and metadata.get("source")
    })
