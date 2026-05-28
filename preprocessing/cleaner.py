import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Auto-download NLTK dependencies on import
def setup_nltk():
    for dep in ['punkt', 'stopwords', 'wordnet', 'punkt_tab']:
        try:
            nltk.download(dep, quiet=True)
        except Exception as e:
            print(f"NLTK dependency {dep} download warning: {e}")

setup_nltk()

try:
    STOPWORDS = set(stopwords.words('english'))
except Exception:
    STOPWORDS = set()

STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()

def clean_text(text: str, use_stemming=False, use_lemmatization=True) -> str:
    """
    Cleans raw text for NLP models:
    1. Case folding (lowercasing)
    2. Stripping punctuation and numeric structures
    3. Tokenizing
    4. Removing stop words
    5. Applying Lemmatization (recommended) or Stemming
    """
    if not text or not isinstance(text, str):
        return ""
    
    # 1 & 2: Lowercasing and scrubbing non-alphabetic characters
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # 3. Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
        
    # 4 & 5: Filter stopwords and reduce word forms
    cleaned = []
    for token in tokens:
        if token not in STOPWORDS and len(token) > 2:
            processed = token
            if use_lemmatization:
                try:
                    processed = LEMMATIZER.lemmatize(processed)
                except Exception:
                    pass
            elif use_stemming:
                try:
                    processed = STEMMER.stem(processed)
                except Exception:
                    pass
            cleaned.append(processed)
            
    return " ".join(cleaned)
