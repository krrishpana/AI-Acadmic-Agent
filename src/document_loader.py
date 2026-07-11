import os
from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return ""
    
    documents_with_metadata = []
    filename = os.path.basename(file_path)

    try:
        reader = PdfReader(file_path)
        
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                documents_with_metadata.append({
                    "text": text,
                    "metadata": {
                        "source": filename,
                        "page": page_idx + 1  
                    }
                })

        return documents_with_metadata
    
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return ""

    