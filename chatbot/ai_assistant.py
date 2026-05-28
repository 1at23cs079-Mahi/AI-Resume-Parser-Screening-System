import re
import sqlite3
import json
from config import Config

def process_recruiter_query(query: str) -> str:
    """
    Parses natural language recruiter questions, maps them to database intents, 
    and returns intelligent recruitment advice and queries.
    """
    query_lower = query.lower().strip()
    
    # Connect to database to query candidates
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, domain, score, text, skills_list, experience_years, education, certifications FROM candidates")
    candidates = [dict(r) for r in cursor.fetchall()]
    conn.close()
    
    if not candidates:
        return "I couldn't find any candidate resumes stored in the database. Please upload a few resumes first!"
        
    # INTENT 1: "Show top Python/Java/etc candidates"
    match_top_skill = re.search(r'show\s+top\s+([a-zA-Z0-9\+\#\.\-]+)\s+candidates', query_lower)
    if match_top_skill:
        skill = match_top_skill.group(1)
        # Filter candidates possessing this skill
        matched = []
        for c in candidates:
            skills_lower = c['skills_list'].lower().split(',') if c['skills_list'] else []
            if skill in skills_lower or skill in c['text'].lower():
                matched.append(c)
                
        if not matched:
            return f"No candidates currently match the skill '{skill}'. Double-check your candidate roster."
            
        # Sort by score
        matched.sort(key=lambda x: x['score'], reverse=True)
        resp = f"### Top Candidates for **{skill.upper()}**:\n\n"
        for i, c in enumerate(matched[:3]):
            resp += f"{i+1}. **{c['name']}** (Score: {c['score']}/10, Exp: {c['experience_years']} yrs) - *Domain: {c['domain']}*\n"
        return resp
        
    # INTENT 2: "Who has cloud certifications?"
    if 'certification' in query_lower or 'certified' in query_lower:
        matched = [c for c in candidates if c['certifications'] and len(c['certifications'].strip()) > 3]
        if not matched:
            return "No candidates are currently listed with active certifications in their profiles."
            
        resp = "### Candidates with Active Professional Certifications:\n\n"
        for c in matched:
            resp += f"- **{c['name']}** holds: *\"{c['certifications']}\"* (Domain: {c['domain']})\n"
        return resp
        
    # INTENT 3: "Find resumes matching 80% of JD"
    match_jd_percent = re.search(r'match(?:ing)?\s*(\d+)%', query_lower)
    if match_jd_percent:
        pct = float(match_jd_percent.group(1))
        # Filter candidates who have score matching the scaled percent
        # E.g. 80% match maps roughly to score >= 8.0
        score_thresh = pct / 10.0
        matched = [c for c in candidates if c['score'] >= score_thresh]
        if not matched:
            return f"No candidates meet the high threshold of a {pct}% alignment rating."
            
        resp = f"### Candidates Matching >= {pct}% of Qualifications:\n\n"
        for c in matched:
            resp += f"- **{c['name']}** (Score: {c['score']}/10, Exp: {c['experience_years']} yrs)\n"
        return resp
        
    # INTENT 4: "Suggest interview questions for [Name]"
    match_interview = re.search(r'(?:suggest\s+)?interview\s+questions\s+for\s+([a-zA-Z\s\.\-]+)', query_lower)
    if match_interview:
        name_query = match_interview.group(1).strip()
        matched_candidate = None
        for c in candidates:
            if name_query in c['name'].lower():
                matched_candidate = c
                break
                
        if not matched_candidate:
            return f"I couldn't find a candidate matching the name '{name_query}' in the database."
            
        return generate_custom_questions(matched_candidate)
        
    # INTENT 5: "Summarize candidate [Name]"
    match_sum = re.search(r'summarize\s+(?:candidate\s+)?([a-zA-Z\s\.\-]+)', query_lower)
    if match_sum:
        name_query = match_sum.group(1).strip()
        matched_candidate = None
        for c in candidates:
            if name_query in c['name'].lower():
                matched_candidate = c
                break
                
        if not matched_candidate:
            return f"I couldn't find a candidate matching the name '{name_query}'."
            
        return f"### Candidate Summary: **{matched_candidate['name']}**\n" \
               f"- **Job Domain:** {matched_candidate['domain']}\n" \
               f"- **Overall Screening Score:** {matched_candidate['score']}/10\n" \
               f"- **Experience:** {matched_candidate['experience_years']} Years\n" \
               f"- **Education:** {matched_candidate['education']}\n" \
               f"- **Certifications:** {matched_candidate['certifications'] or 'None listed'}\n" \
               f"- **Linguistic Skills:** {matched_candidate['skills_list'] or 'General'}\n"
               
    # INTENT 6: "Show top candidates"
    if 'top' in query_lower or 'best' in query_lower or 'rank' in query_lower:
        candidates.sort(key=lambda x: x['score'], reverse=True)
        resp = "### Candidate Leaderboard Rankings:\n\n"
        for i, c in enumerate(candidates[:5]):
            resp += f"{i+1}. **{c['name']}** (Score: {c['score']}/10) - *{c['domain']} Specialist* (Experience: {c['experience_years']} yrs)\n"
        return resp
        
    # Fallback general query assistance
    return "I am your AI Recruiter Assistant. Try asking me:\n" \
           "- *\"Show top python candidates\"*\n" \
           "- *\"Who has active certifications?\"*\n" \
           "- *\"Summarize candidate Sarah Miller\"*\n" \
           "- *\"Suggest interview questions for Sarah Miller\"*\n" \
           "- *\"Find candidates matching 80%\"*"

def generate_custom_questions(c: dict) -> str:
    """
    Generates targeted technical interview questions based on candidate domain and skills.
    """
    domain = c['domain']
    skills = c['skills_list'].split(',') if c['skills_list'] else []
    
    questions = f"### Interview Prep for **{c['name']}** ({domain}):\n\n"
    questions += f"**Background:** Candidate possesses {c['experience_years']} years experience with a {c['education']}.\n\n"
    
    if domain == "Data Science":
        questions += "1. *\"We noticed you have hands-on experience with K-Means clustering. Can you describe how you compute cluster centroids and choose optimal 'K' values?\"*\n"
        questions += "2. *\"Your profile highlights deep learning frameworks. How do you prevent overfitting in deep neural networks?\"*\n"
    elif domain == "Web Development":
        questions += "1. *\"You have built single page applications. How do React Virtual DOM operations differ from standard HTML browser DOM renderings?\"*\n"
        questions += "2. *\"Can you explain your experience configuring secure RESTful microservices and managing CORS requests?\"*\n"
    elif domain == "DevOps":
        questions += "1. *\"Describe a scenario where you wrote Infrastructure as Code using Terraform. How did you manage state files?\"*\n"
        questions += "2. *\"How do you orchestrate Docker containers in large Kubernetes clusters?\"*\n"
    else:
        questions += "1. *\"Can you explain the most challenging project listed in your resume and your technical architecture choices?\"*\n"
        questions += "2. *\"Given your years of experience, how do you handle scaling bottlenecks in production environments?\"*\n"
        
    return questions
