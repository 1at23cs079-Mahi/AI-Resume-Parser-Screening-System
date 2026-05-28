import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Dynamic download of NLTK datasets
def init_nltk_corpora():
    for res in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
        try:
            nltk.download(res, quiet=True)
        except Exception as e:
            print(f"Error downloading NLTK corpus {res}: {e}")

init_nltk_corpora()

try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = set()

STEMMER = PorterStemmer()
LEMMATIZER = WordNetLemmatizer()

def clean_resume_text(text: str, apply_stemming=False, apply_lemmatization=True) -> str:
    """
    Step 2: NLP Preprocessing Pipeline.
    Cleans raw resume text by executing:
    - Lowercasing
    - Removing URLs, emails, and web links
    - Removing digits / numbers
    - Removing punctuation and special characters
    - Tokenization
    - Removing standard NLTK English stopwords
    - Dynamic Lemmatization or Stemming
    """
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Remove URLs / Links
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    
    # 3. Remove email structures
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' ', text)
    
    # 4. Remove numbers / digits
    text = re.sub(r'\d+', ' ', text)
    
    # 5. Remove punctuation and special characters (keep alphabets and spaces)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # 6. Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
        
    # 7. Filter Stopwords & Apply Stemming/Lemmatization
    processed_tokens = []
    for token in tokens:
        # Ignore extremely short strings and standard stopwords
        if token not in STOP_WORDS and len(token) > 2:
            word = token
            if apply_lemmatization:
                try:
                    word = LEMMATIZER.lemmatize(word)
                except Exception:
                    pass
            elif apply_stemming:
                try:
                    word = STEMMER.stem(word)
                except Exception:
                    pass
            processed_tokens.append(word)
            
    return " ".join(processed_tokens)
