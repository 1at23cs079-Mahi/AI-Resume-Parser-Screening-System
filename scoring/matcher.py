import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing.cleaner import clean_text

def match_job_description(resume_text: str, jd_text: str) -> dict:
    """
    Computes semantic similarity, keyword overlap percentage, and missing skills 
    between an incoming candidate resume and a recruiter-provided Job Description.
    """
    if not jd_text.strip():
        return {
            "similarity_score": 0.0,
            "overlap_percentage": 0.0,
            "matched_terms": [],
            "missing_terms": []
        }
        
    # 1. Preprocess texts
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(jd_text)
    
    # 2. Compute Cosine Similarity using TF-IDF
    vectorizer = TfidfVectorizer(max_features=250)
    try:
        tfidf = vectorizer.fit_transform([clean_resume, clean_jd])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    except Exception:
        sim = 0.1 # fallback
        
    # Scale cosine similarity (typically sparse, maps perfectly with standard coefficients)
    similarity_score = float(round(min(sim * 100 * 1.5, 100.0), 1))
    
    # 3. Extract key skill terms from the JD to check overlap
    # Standard tech/business core term lookup
    skills_vocab = {
        'python', 'java', 'c++', 'javascript', 'typescript', 'sql', 'r', 'julia', 'go', 'rust', 'ruby',
        'tensorflow', 'pytorch', 'keras', 'scikit', 'sklearn', 'pandas', 'numpy', 'scipy',
        'react', 'angular', 'vue', 'node', 'express', 'django', 'fastapi', 'flask', 'spring',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'terraform', 'ansible',
        'wireshark', 'metasploit', 'splunk', 'siem', 'penetration', 'security', 'cissp', 'ceh', 'firewall',
        'leadership', 'agile', 'scrum', 'recruitment', 'marketing', 'sales', 'management'
    }
    
    jd_words = set(re.findall(r'\b[a-zA-Z]{2,}\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z]{2,}\b', resume_text.lower()))
    
    # Identify vocab terms present in the JD
    jd_skills = jd_words.intersection(skills_vocab)
    resume_skills = resume_words.intersection(skills_vocab)
    
    matched = list(jd_skills.intersection(resume_skills))
    missing = list(jd_skills.difference(resume_skills))
    
    overlap = 0.0
    if jd_skills:
        overlap = float(round((len(matched) / len(jd_skills)) * 100.0, 1))
        
    return {
        "similarity_score": similarity_score,
        "overlap_percentage": overlap,
        "matched_terms": matched,
        "missing_terms": missing
    }
