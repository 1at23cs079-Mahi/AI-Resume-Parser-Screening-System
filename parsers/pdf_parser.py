import pypdf

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text content from a PDF file using pypdf.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error parsing PDF file {file_path}: {e}")
        raise ValueError(f"Failed to parse PDF document: {e}")
        
    return text
