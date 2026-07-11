def split_text(docs_with_metadata: list[dict], chunk_size: int = 500, chunk_overlap: int =50)-> list:

    chunked_records = []
    
    for docs in docs_with_metadata:
        text = docs["text"]
        meta = docs["metadata"]

        start = 0
        text_length = len(text)
        chunk_idx = 0

        while start < text_length:
            end = start + chunk_size
            chunk_text = text[start:end]
            
            # Create a unique copy of the metadata dictionary for this specific slice
            chunk_meta = meta.copy()
            chunk_meta["chunk_id"] = chunk_idx
            
            chunked_records.append({
                "text": chunk_text,
                "metadata": chunk_meta
            })
            
            start += (chunk_size - chunk_overlap)
            chunk_idx += 1

    return chunked_records

