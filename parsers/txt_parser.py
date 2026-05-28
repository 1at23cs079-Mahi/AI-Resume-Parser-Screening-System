def extract_text_from_txt(file_path: str) -> str:
    """
    Extracts text from plain text (.txt) files.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT file {file_path}: {e}")
        raise ValueError(f"Failed to read TXT document: {e}")
