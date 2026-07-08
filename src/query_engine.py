def search_database(collection, query_vector: list[float], top_k: int = 3) -> list[str]:

    if not query_vector:
        return []
    try:
        results = collection.query(
            query_embeddings=query_vector,
            n_results=top_k
        )

        if results and results.get("documents") and len(results["documents"]) > 0:
            return results["documents"][0]
        
        return []

    except Exception as e:
        print(f"Error querying the vector store: {e}")
        return []

