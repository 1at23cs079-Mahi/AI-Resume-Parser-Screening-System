import os
import re
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename: str) -> bool:
    """
    Checks if the uploaded file has a valid permitted extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_and_sanitize_filename(filename: str) -> str:
    """
    Sanitizes filenames to prevent path traversal vulnerabilities.
    """
    clean_name = secure_filename(filename)
    if not clean_name:
        return "unnamed_resume.txt"
    return clean_name

def sql_injection_check(user_input: str) -> bool:
    """
    Scans inputs for common SQL injection keywords to prevent injection vectors.
    """
    if not user_input or not isinstance(user_input, str):
        return False
    # Common SQL Injection patterns
    patterns = [
        r"union\s+select",
        r"select\s+.*\s+from",
        r"insert\s+into",
        r"delete\s+from",
        r"drop\s+table",
        r"update\s+.*\s+set",
        r"'\s*or\s*'\s*\d+\s*=\s*\d+",
        r"\"\s*or\s*\"\s*\d+\s*=\s*\d+",
        r"--",
        r";\s*$"
    ]
    for pattern in patterns:
        if re.search(pattern, user_input.lower()):
            return True
    return False
