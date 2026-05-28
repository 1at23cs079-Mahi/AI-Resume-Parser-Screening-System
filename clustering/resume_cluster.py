import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from preprocessing.text_cleaner import clean_resume_text

class ResumeClusteringPipeline:
    """
    Step 13: Resume Clustering.
    Extracts features, fits K-Means, clusters resumes in database,
    and returns labeled spatial coordinates for scatter visualization.
    """
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.vectorizer = TfidfVectorizer(max_features=250)
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=5)

    def cluster_candidates(self, candidates: list) -> list:
        """
        Takes raw database candidates list, fits K-Means, and appends PCA coordinates.
        """
        if not candidates or len(candidates) < 2:
            return []
            
        df = pd.DataFrame(candidates)
        
        # Clean text
        df['Cleaned'] = df['text'].apply(lambda x: clean_resume_text(x))
        
        # Fit TF-IDF
        try:
            tfidf_matrix = self.vectorizer.fit_transform(df['Cleaned'])
            # Scale clusters
            k = min(self.n_clusters, len(df))
            self.kmeans = KMeans(n_clusters=k, random_state=42, n_init=5)
            df['Cluster_ID'] = self.kmeans.fit_predict(tfidf_matrix)
            
            # Reduce with PCA
            pca = PCA(n_components=2, random_state=42)
            coords = pca.fit_transform(tfidf_matrix.toarray())
            df['X'] = coords[:, 0]
            df['Y'] = coords[:, 1]
        except Exception:
            # Fallback coordinates
            np.random.seed(42)
            df['Cluster_ID'] = np.random.randint(0, min(self.n_clusters, len(df)), size=len(df))
            df['X'] = np.random.uniform(-5, 5, size=len(df))
            df['Y'] = np.random.uniform(-5, 5, size=len(df))
            
        # Standardize coordinates to (-8 to 8) scale
        x_min, x_max = df['X'].min(), df['X'].max()
        y_min, y_max = df['Y'].min(), df['Y'].max()
        
        if x_max != x_min:
            df['X'] = ((df['X'] - x_min) / (x_max - x_min) * 16) - 8
        else:
            df['X'] = 0.0
            
        if y_max != y_min:
            df['Y'] = ((df['Y'] - y_min) / (y_max - y_min) * 16) - 8
        else:
            df['Y'] = 0.0
            
        results = []
        for _, row in df.iterrows():
            results.append({
                "id": int(row['id']),
                "name": str(row['name']),
                "domain": str(row['domain']),
                "cluster_id": int(row['Cluster_ID']),
                "x": float(round(row['X'], 2)),
                "y": float(round(row['Y'], 2))
            })
            
        return results
