import os

class Config:
    # Secret Key for sessions
    SECRET_KEY = os.environ.get('SECRET_KEY', 'recruitment_intelligence_platform_secret_key_2026')
    
    # Base Workspace path
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Check if running on Vercel
    IS_VERCEL = os.environ.get('VERCEL') == '1' or 'VERCEL' in os.environ
    
    if IS_VERCEL:
        DATABASE = '/tmp/recruitment_intelligence.db'
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        # SQLite Database URI
        DATABASE = os.path.join(BASE_DIR, 'database', 'recruitment_intelligence.db')
        # Upload Configurations
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
        
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # Strict Max upload: 5 Megabytes
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg'}
    
    # Model Thresholds
    ATS_MIN_ACCEPTABLE_SCORE = 50.0
    COSINE_SIMILARITY_THRESHOLD = 0.40

