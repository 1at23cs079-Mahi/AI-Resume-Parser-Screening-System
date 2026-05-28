import os
import re
import collections
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Ensure NLTK resources are downloaded
def download_nltk_resources():
    for res in ["punkt", "stopwords", "wordnet", "punkt_tab"]:
        try:
            nltk.download(res, quiet=True)
        except Exception as e:
            print(f"Failed to download NLTK resource {res}: {e}")

download_nltk_resources()

# Load NLTK stop words and lemmatizer
try:
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    STOP_WORDS = set()
LEMMATIZER = WordNetLemmatizer()

def preprocess_text(text: str) -> str:
    """
    Standard text preprocessing pipeline:
    - Lowercase text
    - Remove punctuation, special characters, and numbers
    - Tokenize
    - Filter stop words
    - Lemmatize
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Lowercase & clean special characters
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # Tokenize
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    
    # Stopwords filter & Lemmatization
    cleaned_tokens = []
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            try:
                lemma = LEMMATIZER.lemmatize(token)
            except Exception:
                lemma = token
            cleaned_tokens.append(lemma)
            
    return " ".join(cleaned_tokens)

# Skill categories and predefined representative keyword clusters (for scoring fallback & enhancement)
SKILL_CLUSTERS = {
    "Data Science": {
        "programming": {"python", "r", "julia", "sql", "scala"},
        "libraries": {"pandas", "numpy", "scipy", "scikit", "sklearn", "matplotlib", "seaborn"},
        "ml_dl": {"machine", "learning", "deep", "neural", "network", "tensorflow", "pytorch", "keras", "clustering", "regression", "classification"},
        "tools": {"jupyter", "spark", "hadoop", "tableau", "powerbi", "aws", "gcp", "git"}
    },
    "Web Development": {
        "languages": {"javascript", "typescript", "html", "css", "python", "php", "ruby"},
        "frontend": {"react", "angular", "vue", "redux", "zustand", "tailwind", "bootstrap", "sass", "webpack", "vite"},
        "backend": {"node", "express", "django", "flask", "fastapi", "spring", "laravel"},
        "database_devops": {"mongodb", "postgresql", "mysql", "redis", "docker", "kubernetes", "aws", "git", "ci", "cd"}
    },
    "HR": {
        "core": {"recruitment", "talent", "acquisition", "onboarding", "relations", "payroll", "policy", "compliance", "retention"},
        "management": {"strategic", "performance", "conflict", "resolution", "leadership", "training", "development"},
        "tools": {"ats", "workday", "bamboohr", "greenhouse", "lever", "excel", "linkedin"}
    },
    "Sales": {
        "core": {"sales", "pipeline", "negotiation", "acquisition", "outreach", "cold", "b2b", "prospecting", "leads", "closing"},
        "marketing": {"seo", "sem", "digital", "campaign", "analytics", "cro", "social", "media", "content", "email"},
        "tools": {"salesforce", "hubspot", "crm", "excel", "linkedin", "google", "ads"}
    }
}

class ResumeParserModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.kmeans = None
        self.categories = []
        self.category_centroids = {}
        self.trained = False

    def train(self, df: pd.DataFrame):
        """
        Train the model using TF-IDF and cluster the skills of each job category.
        """
        if df.empty:
            return
        
        # Preprocess dataset resumes
        df["Processed_Resume"] = df["Resume"].apply(preprocess_text)
        
        # Fit TF-IDF Vectorizer
        tfidf_matrix = self.vectorizer.fit_transform(df["Processed_Resume"])
        
        # Group by Category and compute centroids
        self.categories = df["Category"].unique().tolist()
        for cat in self.categories:
            cat_indices = df[df["Category"] == cat].index
            cat_vectors = tfidf_matrix[cat_indices]
            # Mean vector for the category
            centroid = np.array(cat_vectors.mean(axis=0)).flatten()
            self.category_centroids[cat] = centroid
            
        # Fit KMeans for grouping keywords/resumes globally
        n_clusters = min(5, len(df))
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.kmeans.fit(tfidf_matrix)
        
        self.trained = True
        print("Model trained successfully!")

    def calculate_score(self, resume_text: str, target_category: str) -> dict:
        """
        Assigns a score from 0 to 10 for a resume against a target category.
        Detects keyword stuffing and penalizes it.
        """
        if not self.trained:
            return {"score": 0.0, "details": "Model not trained"}
        
        # Clean text
        raw_words = re.findall(r'[a-zA-Z]+', resume_text.lower())
        processed_resume = preprocess_text(resume_text)
        
        if not processed_resume:
            return {
                "score": 0.0,
                "breakdown": {
                    "semantic_similarity": 0,
                    "skill_coverage": 0,
                    "formatting_bonus": 0,
                    "keyword_stuffing_penalty": 0
                },
                "feedback": "Empty or invalid resume text."
            }
        
        # 1. Semantic Similarity to Category Centroid
        resume_tfidf = self.vectorizer.transform([processed_resume]).toarray().flatten()
        
        if target_category in self.category_centroids:
            centroid = self.category_centroids[target_category]
            # Compute cosine similarity
            sim = cosine_similarity([resume_tfidf], [centroid])[0][0]
        else:
            sim = 0.1 # default fallback
            
        # Normalize similarity (typically ranges from 0 to 0.6 in sparse TF-IDF)
        semantic_score = min(sim * 15, 10.0)
        
        # 2. Skill Coverage (checking presence of relevant skills categories)
        coverage_score = 0.0
        matched_skills = {}
        category_clusters = SKILL_CLUSTERS.get(target_category, {})
        
        if category_clusters:
            total_groups = len(category_clusters)
            matched_groups = 0
            for group, keywords in category_clusters.items():
                matched_in_group = [w for w in raw_words if w in keywords]
                if matched_in_group:
                    matched_groups += 1
                    matched_skills[group] = list(set(matched_in_group))
            
            coverage_score = (matched_groups / total_groups) * 10.0
        else:
            # Fallback based on unique tokens match
            coverage_score = min(len(set(processed_resume.split())) / 10, 10.0)
            
        # 3. Formatting & Structure Bonus
        formatting_score = 10.0
        # Check contact info elements (email, phone, etc.)
        has_email = 1 if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text) else 0
        has_phone = 1 if re.search(r'\+?\d[\d -]{8,12}\d', resume_text) else 0
        
        formatting_score = (has_email * 5.0) + (has_phone * 3.0) + (2.0 if len(resume_text.split()) > 40 else 0)
        
        # 4. Keyword Overstuffing Penalty (CRITICAL DETECTOR)
        # Calculates word repetition. If a word makes up a huge percentage of the resume, or is repeated consecutively.
        word_counts = collections.Counter(processed_resume.split())
        total_tokens = len(processed_resume.split())
        
        penalty = 0.0
        stuffing_detected = False
        stuffed_words = []
        
        if total_tokens > 0:
            for word, count in word_counts.items():
                # If a single word represents more than 6% of processed text and is a key skill word, it is likely stuffed
                freq = count / total_tokens
                if freq > 0.07 and count > 3:
                    penalty += (freq - 0.07) * 40.0 # aggressive scaling penalty
                    stuffing_detected = True
                    stuffed_words.append(f"'{word}' ({count} times)")
                    
        # Check for exact consecutive repeat stuffers: e.g., "python python python"
        consecutive_repeats = re.findall(r'\b([a-zA-Z]+)\s+\1\s+\1\b', resume_text.lower())
        if consecutive_repeats:
            penalty += len(consecutive_repeats) * 2.0
            stuffing_detected = True
            stuffed_words.extend([f"consecutive repetition of '{w}'" for w in set(consecutive_repeats)])
            
        penalty = min(penalty, 8.0) # max penalty cap
        
        # Calculate final weighted score out of 10
        # 40% Semantic Similarity, 40% Skill Coverage, 20% Formatting
        base_score = (semantic_score * 0.4) + (coverage_score * 0.4) + (formatting_score * 0.2)
        final_score = max(0.0, min(10.0, base_score - penalty))
        
        # Generate dynamic qualitative feedback
        if stuffing_detected:
            feedback = f"Warning: Potential keyword stuffing or excessive term repetition detected: {', '.join(stuffed_words)}. Re-evaluate authenticity."
        elif final_score >= 8.0:
            feedback = "Excellent alignment of semantic context and complete skill profile. Highly favorable candidate."
        elif final_score >= 5.0:
            feedback = "Moderate match. Good skill foundation, but could emphasize more industry-related concepts or tools."
        else:
            feedback = "Low alignment. Resume misses essential core concepts or is too brief to evaluate properly."
            
        return {
            "score": round(final_score, 1),
            "breakdown": {
                "semantic_similarity": round(semantic_score, 1),
                "skill_coverage": round(coverage_score, 1),
                "formatting_bonus": round(formatting_score, 1),
                "keyword_stuffing_penalty": round(penalty, 1)
            },
            "matched_skills": matched_skills,
            "stuffed_words": stuffed_words,
            "feedback": feedback
        }

    def get_skill_clusters_visualization(self, category: str) -> dict:
        """
        Returns visualizable data representing word grouping clusters for the UI.
        """
        clusters = SKILL_CLUSTERS.get(category, {})
        viz_data = []
        for cluster_name, words in clusters.items():
            for word in words:
                viz_data.append({
                    "word": word,
                    "cluster": cluster_name,
                    "val": np.random.randint(15, 30) # standard sizes for bubble map
                })
        return {"category": category, "skills": viz_data}
