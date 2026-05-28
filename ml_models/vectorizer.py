import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfFeatureExtractor:
    """
    Step 3: Feature Extraction.
    Uses TF-IDF Vectorization with max features optimization and n-grams to extract
    sparse feature matrices and saves the fitted vectorizer as tfidf_vectorizer.pkl.
    """
    def __init__(self, max_features=1500, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True
        )
        self.fitted = False

    def fit_transform(self, corpus: list):
        """
        Fits vectorizer and returns sparse term-frequency matrices.
        """
        tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.fitted = True
        return tfidf_matrix

    def transform(self, texts: list):
        """
        Transforms text arrays using the saved vectorizer state.
        """
        if not self.fitted:
            raise ValueError("TF-IDF Vectorizer has not been fitted yet!")
        return self.vectorizer.transform(texts)

    def save_vectorizer(self, dest_path='models/tfidf_vectorizer.pkl'):
        """
        Saves the fitted vectorizer state.
        """
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        print(f"TF-IDF Vectorizer successfully saved to {dest_path}")

    def load_vectorizer(self, src_path='models/tfidf_vectorizer.pkl'):
        """
        Loads the fitted vectorizer state.
        """
        if os.path.exists(src_path):
            with open(src_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.fitted = True
            print(f"TF-IDF Vectorizer loaded successfully from {src_path}")
        else:
            raise FileNotFoundError(f"TF-IDF Vectorizer not found at {src_path}")
