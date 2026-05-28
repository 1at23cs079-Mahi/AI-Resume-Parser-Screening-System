import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from preprocessing.cleaner import clean_text

def get_resume_clusters():
    """
    Groups all candidate resumes in the database dynamically using K-Means.
    Reduces dimensions with PCA to map candidates onto 2D (X, Y) coordinates for Chart.js display.
    """
    import sqlite3
    from config import Config
    
    conn = sqlite3.connect(Config.DATABASE)
    df = pd.read_sql_query("SELECT id, name, domain, text FROM candidates", conn)
    conn.close()
    
    if df.empty:
        return []
    
    # 1. Clean resumes
    df['Cleaned'] = df['text'].apply(lambda x: clean_text(x))
    
    # 2. Extract TF-IDF weights
    vectorizer = TfidfVectorizer(max_features=200)
    tfidf_matrix = vectorizer.fit_transform(df['Cleaned'])
    
    # 3. K-Means Clustering (K = 3 or 4 based on dataset size)
    n_clusters = min(4, len(df))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=5)
    df['Cluster'] = kmeans.fit_predict(tfidf_matrix)
    
    # 4. Dimensionality Reduction with PCA
    try:
        pca = PCA(n_components=2, random_state=42)
        coords = pca.fit_transform(tfidf_matrix.toarray())
        df['X'] = coords[:, 0]
        df['Y'] = coords[:, 1]
    except Exception:
        # Fallback pseudo-PCA coordinates if matrix is too small/singular
        np.random.seed(42)
        df['X'] = np.random.uniform(-1, 1, size=len(df))
        df['Y'] = np.random.uniform(-1, 1, size=len(df))
        
    # Scale coordinates for beautiful UI chart presentation (-10 to 10 scale)
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
        
    # Prepare JSON serializable list for dashboard plotting
    clusters_data = []
    for _, row in df.iterrows():
        clusters_data.append({
            "id": int(row['id']),
            "name": str(row['name']),
            "domain": str(row['domain']),
            "cluster_id": int(row['Cluster']),
            "x": float(round(row['X'], 2)),
            "y": float(round(row['Y'], 2))
        })
        
    return clusters_data
