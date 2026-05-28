import re
from database.db_manager import get_scoring_weights
from scoring.ats_simulator import analyze_ats_compliance
from scoring.scorer import extract_candidate_entities, SKILL_MAPS

def compute_weighted_ranking_score(resume_text: str, target_domain: str) -> dict:
    """
    Step 8: Weighted Scoring Engine.
    Executes the exact multi-factor dynamic mathematical formula specified in requirements:
      Final Score = (Skills * 0.40) + (Experience * 0.25) + (Education * 0.15) + (Certifications * 0.10) + (Projects * 0.10)
    Converts overall fit to 0-10 scale and maps it for leaderboard rankings.
    """
    # 1. Parse entities and structure checks
    entities = extract_candidate_entities(resume_text)
    ats_results = analyze_ats_compliance(resume_text)
    
    # Retrieve configurations
    weights = get_scoring_weights()
    w_skills = weights.get("skill_weight", 0.40)
    w_exp = weights.get("experience_weight", 0.25)
    w_edu = weights.get("education_weight", 0.15)
    w_cert = weights.get("certification_weight", 0.10)
    w_proj = weights.get("project_weight", 0.10)
    
    # Calculations:
    # 1. Skills (0-10 scale): unique technology tokens
    total_found = []
    matched_skills = {}
    text_lower = resume_text.lower()
    
    for category, skills in SKILL_MAPS.items():
        found = [s for s in skills if re.search(r'\b' + re.escape(s) + r'\b', text_lower)]
        if found:
            matched_skills[category] = found
            total_found.extend(found)
            
    skills_score = min(len(total_found) * 1.2, 10.0)
    
    # 2. Experience: scaled up to 5 years ideal experience
    exp_score = min((entities["experience_years"] / 5.0) * 10.0, 10.0)
    
    # 3. Education: Ph.D.=10, Master=9, Bachelor=8, other=5
    edu_tiers = {
        "Ph.D.": 10.0,
        "Master's Degree": 9.0,
        "Bachelor's Degree": 8.0,
        "High School / Associate": 5.0
    }
    edu_score = edu_tiers.get(entities["education"], 5.0)
    
    # 4. Certifications
    cert_score = min(entities["certifications_count"] * 2.5, 10.0)
    
    # 5. Projects
    proj_score = min(entities["projects_count"] * 2.0, 10.0)
    
    # Sum weighted core factors
    base_score = (skills_score * w_skills) + \
                 (exp_score * w_exp) + \
                 (edu_score * w_edu) + \
                 (cert_score * w_cert) + \
                 (proj_score * w_proj)
                 
    # Deduct stuffing penalty if flagged
    penalty = 0.0
    if ats_results["overstuffing_warning"]:
        penalty = min(ats_results["ats_score"] / 20.0, 3.5)
        
    final_score = max(0.0, min(10.0, base_score - penalty))
    
    return {
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
            "keyword_stuffing_penalty": round(penalty, 1)
        },
        "ats_details": ats_results
    }
