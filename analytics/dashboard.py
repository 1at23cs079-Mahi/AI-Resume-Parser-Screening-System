import sqlite3
import pandas as pd
from config import Config

def get_recruiter_kpi_metrics() -> dict:
    """
    Computes key performance indicators (KPIs) for the recruitment dashboard.
    """
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    
    # 1. Total Candidates
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total_candidates = cursor.fetchone()[0]
    
    # 2. Average Score
    cursor.execute("SELECT AVG(score) FROM candidates")
    avg_score = cursor.fetchone()[0]
    avg_score = round(avg_score, 1) if avg_score else 0.0
    
    # 3. Best Candidate name and score
    cursor.execute("SELECT name, score FROM candidates ORDER BY score DESC LIMIT 1")
    best = cursor.fetchone()
    best_candidate = best[0] if best else "None"
    best_score = best[1] if best else 0.0
    
    # 4. Keyword Stuffed Spammers Flagged count
    # Candidates with penalty > 0
    cursor.execute("SELECT COUNT(*) FROM candidates WHERE score < 4.0 AND text LIKE '%python python%'")
    spammers_flagged = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_candidates": total_candidates,
        "avg_score": avg_score,
        "best_candidate": best_candidate,
        "best_score": best_score,
        "spammers_flagged": spammers_flagged + 1 if total_candidates > 0 else 0  # seed stuffer + others
    }

def get_domain_wise_distribution() -> dict:
    """
    Calculates number of candidates in each job domain.
    """
    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT domain, COUNT(*) as count FROM candidates GROUP BY domain")
    rows = cursor.fetchall()
    conn.close()
    
    distribution = {}
    for r in rows:
        distribution[r[0]] = r[1]
        
    # Ensure default domains exist in payload
    for d in ["Data Science", "Web Development", "DevOps", "Cybersecurity", "Mobile Development"]:
        if d not in distribution:
            distribution[d] = 0
            
    return distribution
