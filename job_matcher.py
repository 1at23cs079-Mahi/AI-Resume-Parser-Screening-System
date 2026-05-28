import os
import re
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.text_cleaner import clean_resume_text

# Comprehensive skill dictionaries
TECH_DICTIONARY = {
    'python', 'java', 'sql', 'cpp', 'c++', 'r', 'javascript', 'typescript', 'bash', 'go',
    'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'pandas', 'numpy',
    'react', 'node', 'express', 'django', 'fastapi', 'flask', 'spring',
    'aws', 'docker', 'kubernetes', 'jenkins', 'git', 'terraform', 'ansible',
    'wireshark', 'metasploit', 'splunk', 'siem', 'pentesting', 'cissp', 'ceh'
}

def match_resume_with_job_description(resume_text: str, jd_text: str) -> dict:
    """
    Step 7: Job Description Matching.
    Converts JD using fitted vectorizer, computes TF-IDF cosine similarity,
    calculates vocabulary skill overlap percentage, and maps missing skills.
    """
    if not jd_text.strip():
        return {
            "similarity_score": 0.0,
            "overlap_percentage": 0.0,
            "matched_terms": [],
            "missing_terms": []
        }

    clean_resume = clean_resume_text(resume_text)
    clean_jd = clean_resume_text(jd_text)
    
    vectorizer_path = 'models/tfidf_vectorizer.pkl'
    sim_score = 0.0
    
    # Cosine Similarity
    if os.path.exists(vectorizer_path):
        try:
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            vectors = vectorizer.transform([clean_resume, clean_jd])
            sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            sim_score = float(round(min(sim * 100 * 1.5, 100.0), 1))
        except Exception:
            sim_score = 10.0
    else:
        # Cosine fallback
        words_r = set(clean_resume.split())
        words_j = set(clean_jd.split())
        if words_r and words_j:
            intersect = len(words_r.intersection(words_j))
            union = len(words_r.union(words_j))
            sim_score = float(round((intersect / union) * 100, 1))

    # Skill Overlap & Missing Lists
    jd_words = set(re.findall(r'\b[a-zA-Z\+\#]{2,}\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z\+\#]{2,}\b', resume_text.lower()))
    
    jd_skills = jd_words.intersection(TECH_DICTIONARY)
    resume_skills = resume_words.intersection(TECH_DICTIONARY)
    
    matched = list(jd_skills.intersection(resume_skills))
    missing = list(jd_skills.difference(resume_skills))
    
    overlap = 0.0
    if jd_skills:
        overlap = float(round((len(matched) / len(jd_skills)) * 100, 1))
        
    return {
        "similarity_score": sim_score,
        "overlap_percentage": overlap,
        "matched_terms": matched,
        "missing_terms": missing
    }
