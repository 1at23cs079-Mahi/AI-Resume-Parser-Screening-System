import docx2txt

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text content from a DOCX file using docx2txt.
    """
    try:
        text = docx2txt.process(file_path)
        return text if text else ""
    except Exception as e:
        print(f"Error parsing DOCX file {file_path}: {e}")
        raise ValueError(f"Failed to parse DOCX document: {e}")
