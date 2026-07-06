import os
from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    if not os.path.exists(file_path):
        print(f"The file {file_path} does not exist.")
        return ""

    try:
        reader = PdfReader(file_path)
        extracted_text = ""

        for page in reader.pages:
            text= page.extract_text()

            if text:
                extracted_text += text + "\n"

        return extracted_text
    
    except Exception as e:
        print(f"An error occurred while reading the PDF: {e}")
        return ""

    