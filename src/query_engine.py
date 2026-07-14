def search_database(collection, query_vector: list[float], top_k: int = 3) -> list[str]:

    if not query_vector:
        return []
    try:
        results = collection.query(
            query_embeddings=query_vector,
            n_results=top_k
        )

        retrieved_data = []

        if results and 'documents' in results and results['documents']:
            documents = results["documents"][0]  

            raw_metadatas = results.get('metadatas')
            metadatas_list = raw_metadatas[0] if (raw_metadatas and raw_metadatas[0]) else []

            for idx in range(len(documents)):
                text = documents[idx]
                # Default to an empty dict if metadata is somehow missing
                meta = {}
                if idx < len(metadatas_list) and metadatas_list[idx] is not None:
                    meta = metadatas_list[idx]
                
                retrieved_data.append({
                    "text": text,
                    "metadata": meta
                })
                
        return retrieved_data

    except Exception as e:
        print(f"Error querying the vector store: {e}")
        return []

