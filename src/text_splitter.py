def split_text(text: str, chunk_size: int = 500, chunk_overlap: int =50)-> list:

    if not text.strip():
        return []
    
    words = text.split()
    chunks = []

    step = chunk_size - chunk_overlap

    if step <= 0:
        print("Warning: chunk_overlap must be smaller than chunk_size. Resetting overlap to 0.")
        step = chunk_size
        chunk_overlap = 0

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks