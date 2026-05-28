import re
import sqlite3
from config import Config
from database.db_manager import get_scoring_weights
from scoring.ats_simulator import analyze_ats_compliance

# Full tech skill categories dictionary (for category segment checks)
SKILL_MAPS = {
    "Programming Languages": {"python", "javascript", "typescript", "sql", "java", "cpp", "c++", "ruby", "julia", "rust", "go", "scala", "bash", "r"},
    "Frameworks": {"react", "next", "redux", "express", "node", "django", "flask", "fastapi", "spring", "laravel", "vue", "angular"},
    "Databases": {"postgresql", "mysql", "sqlite", "mongodb", "redis", "oracle", "cassandra"},
    "Cloud Platforms": {"aws", "azure", "gcp", "google cloud", "heroku", "digitalocean", "lambda"},
    "DevOps Tools": {"docker", "kubernetes", "jenkins", "terraform", "ansible", "git", "gitlab", "jenkins", "ci", "cd"},
    "AI/ML Libraries": {"tensorflow", "pytorch", "keras", "scikit-learn", "sklearn", "pandas", "numpy", "matplotlib", "seaborn", "scipy"}
}

def check_duplicate_resume(resume_text: str) -> bool:
    """
    Checks if a highly similar or identical resume text has already been saved 
    to prevent processing duplicates.
    """
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, text FROM candidates")
    rows = cursor.fetchall()
    conn.close()
    
    # Clean incoming text for comparison
    clean_in = re.sub(r'\s+', '', resume_text.lower()[:300])
    for r_id, raw_text in rows:
        clean_db = re.sub(r'\s+', '', raw_text.lower()[:300])
        if clean_in == clean_db:
            return True
    return False

def extract_candidate_entities(resume_text: str) -> dict:
    """
    Extracts structured metrics using regex and structural contextual searches:
    - Name (Header line heuristic)
    - Email & Phone
    - Education level
    - Certifications count
    - Experience Years (looking for numbers preceding 'years experience' or duration calculations)
    - Project Complexity (projects listed count)
    """
    text_lower = resume_text.lower()
    
    # 1. Contact Details
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text)
    phone_match = re.search(r'\+?\d[\d -]{7,12}\d', resume_text)
    
    email = email_match.group(0) if email_match else "Not Specified"
    phone = phone_match.group(0) if phone_match else "Not Specified"
    
    # 2. Extract Name (Heuristic: First line that isn't email, or standard capitalized header)
    lines = [l.strip() for l in resume_text.split('\n') if l.strip()]
    name = "Candidate Profile"
    if lines:
        for line in lines[:3]:
            # Ensure line does not contain email/phone symbols or long text
            if '@' not in line and not re.search(r'\d{6,}', line) and len(line) < 35:
                name = line
                break
                
    # 3. Experience Years Extraction
    exp_years = 0.0
    # Pattern: '5 years of experience', '7+ years', 'experience: 4 years'
    exp_patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience\s*:\s*(\d+)\+?\s*years?',
        r'(\d+)\s*years?\s+in\s+'
    ]
    for p in exp_patterns:
        match = re.search(p, text_lower)
        if match:
            exp_years = float(match.group(1))
            break
            
    # If no pattern matches, simulate experience based on dates listed (e.g. '2019 - 2023')
    if exp_years == 0.0:
        dates = re.findall(r'\b(20\d{2})\b', text_lower)
        if len(dates) >= 2:
            try:
                unique_dates = sorted(list(set([int(d) for d in dates])))
                span = unique_dates[-1] - unique_dates[0]
                if 0 < span < 15:
                    exp_years = float(span)
            except Exception:
                pass
                
    # 4. Education level check
    education = "High School / Associate"
    if re.search(r'ph\.d|doctorate|doctor\s+of\s+philosophy', text_lower):
        education = "Ph.D."
    elif re.search(r'm\.s\b|master\b|mba\b|post\s*graduate', text_lower):
        education = "Master's Degree"
    elif re.search(r'b\.s\b|b\.e\b|b\.tech|bachelor\b|undergraduate', text_lower):
        education = "Bachelor's Degree"
        
    # 5. Project count check
    # Counts instances of projects listed or keywords
    project_matches = len(re.findall(r'\bproject\b', text_lower))
    projects_count = max(1, min(project_matches, 5)) # scale between 1 and 5
    
    # 6. Certifications listed
    certs = []
    cert_matches = re.findall(r'\b(certified|certification|certificate|cissp|ceh|comptia|aws|azure)\b', text_lower)
    cert_count = len(cert_matches)
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "experience_years": exp_years if exp_years > 0 else 1.0,
        "education": education,
        "projects_count": projects_count,
        "certifications_count": cert_count
    }

def score_candidate(resume_text: str, target_category: str) -> dict:
    """
    Computes a comprehensive weighted candidate score (0 to 10 scale).
    Integrates recruiter weight settings, ATS details, and entities.
    """
    # 1. Run Entity extraction
    entities = extract_candidate_entities(resume_text)
    
    # 2. Run ATS Simulator
    ats_results = analyze_ats_compliance(resume_text)
    
    # 3. Retrieve recruiter configurable weights from database
    weights = get_scoring_weights()
    w_skills = weights.get("skill_weight", 0.40)
    w_exp = weights.get("experience_weight", 0.25)
    w_edu = weights.get("education_weight", 0.15)
    w_cert = weights.get("certification_weight", 0.10)
    w_proj = weights.get("project_weight", 0.10)
    
    # -- 1. Skill Relevance Score (S_skills) --
    # Checks how many matching tech groups the candidate possesses
    matched_skills = {}
    total_found = []
    text_lower = resume_text.lower()
    
    for category, skills in SKILL_MAPS.items():
        found = [s for s in skills if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
        if found:
            matched_skills[category] = found
            total_found.extend(found)
            
    # Skill relevance score bases on unique matching skills count (max 10 points)
    skills_score = min(len(total_found) * 1.2, 10.0)
    
    # -- 2. Experience Relevance Score (S_exp) --
    # We expect 5 years experience as ideal for max points
    exp_score = min((entities["experience_years"] / 5.0) * 10.0, 10.0)
    
    # -- 3. Education Quality Score (S_edu) --
    edu_scores = {
        "Ph.D.": 10.0,
        "Master's Degree": 9.0,
        "Bachelor's Degree": 8.0,
        "High School / Associate": 5.0
    }
    edu_score = edu_scores.get(entities["education"], 5.0)
    
    # -- 4. Certification Relevance (S_cert) --
    cert_score = min(entities["certifications_count"] * 2.5, 10.0)
    
    # -- 5. Project Complexity (S_proj) --
    proj_score = min(entities["projects_count"] * 2.0, 10.0)
    
    # Compute base weighted score
    base_score = (skills_score * w_skills) + \
                 (exp_score * w_exp) + \
                 (edu_score * w_edu) + \
                 (cert_score * w_cert) + \
                 (proj_score * w_proj)
                 
    # Normalize score (0-10) and deduct ATS penalty if keyword stuffing occurred
    ats_penalty = 0.0
    if ats_results["overstuffing_warning"]:
        ats_penalty = min(ats_results["ats_score"] / 20.0, 3.5) # apply up to 3.5 score deduction
        
    final_score = max(0.0, min(10.0, base_score - ats_penalty))
    
    # Integrate entities and scores into a final payload
    candidate_data = {
        "name": entities["name"],
        "email": entities["email"],
        "phone": entities["phone"],
        "text": resume_text,
        "score": round(final_score, 1),
        "ats_score": ats_results["ats_score"],
        "experience_years": entities["experience_years"],
        "projects_count": entities["projects_count"],
        "education": entities["education"],
        "skills_list": total_found,
        "matched_skills": matched_skills,
        "breakdown": {
            "skill_relevance": round(skills_score, 1),
            "experience_score": round(exp_score, 1),
            "education_score": round(edu_score, 1),
            "certification_score": round(cert_score, 1),
            "project_score": round(proj_score, 1),
            "keyword_stuffing_penalty": round(ats_penalty, 1)
        },
        "ats_details": ats_results
    }
    
    return candidate_data
