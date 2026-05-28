import os
import sqlite3
import json
from config import Config

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    os.makedirs(os.path.dirname(Config.DATABASE), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Initializes database tables for candidates, recruiters, and chatbot history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Candidates Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            domain TEXT,
            text TEXT NOT NULL,
            score REAL DEFAULT 0.0,
            ats_score REAL DEFAULT 0.0,
            raw_breakdown TEXT,
            matched_skills TEXT,
            skills_list TEXT,
            source TEXT DEFAULT 'Upload',
            experience_years REAL DEFAULT 0.0,
            projects_count INTEGER DEFAULT 0,
            education TEXT,
            certifications TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Chatbot Logs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chatbot_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Settings / Weights Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scoring_weights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_weight REAL DEFAULT 0.40,
            experience_weight REAL DEFAULT 0.25,
            education_weight REAL DEFAULT 0.15,
            certification_weight REAL DEFAULT 0.10,
            project_weight REAL DEFAULT 0.10
        )
    ''')
    
    # Check if default weights exist, seed them if missing
    cursor.execute("SELECT COUNT(*) FROM scoring_weights")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO scoring_weights (skill_weight, experience_weight, education_weight, certification_weight, project_weight)
            VALUES (0.40, 0.25, 0.15, 0.10, 0.10)
        ''')
        
    conn.commit()
    conn.close()
    print("Database tables initialized successfully.")

def save_candidate(candidate_data: dict) -> int:
    """
    Saves a parsed and scored candidate to the SQLite database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO candidates (
            name, email, phone, domain, text, score, ats_score, 
            raw_breakdown, matched_skills, skills_list, source, 
            experience_years, projects_count, education, certifications
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        candidate_data.get('name', 'Unknown'),
        candidate_data.get('email'),
        candidate_data.get('phone'),
        candidate_data.get('domain', 'General'),
        candidate_data.get('text', ''),
        candidate_data.get('score', 0.0),
        candidate_data.get('ats_score', 0.0),
        json.dumps(candidate_data.get('breakdown', {})),
        json.dumps(candidate_data.get('matched_skills', {})),
        ",".join(candidate_data.get('skills_list', [])),
        candidate_data.get('source', 'Upload'),
        candidate_data.get('experience_years', 0.0),
        candidate_data.get('projects_count', 0),
        candidate_data.get('education', 'Not Specified'),
        candidate_data.get('certifications', '')
    ))
    
    candidate_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return candidate_id

def get_candidates():
    """
    Retrieves all candidates from the database sorted by score descending.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates ORDER BY score DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_candidate_by_id(candidate_id: int):
    """
    Retrieves a single candidate profile.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def save_chatbot_log(sender: str, message: str):
    """
    Saves dialog logs to database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chatbot_logs (sender, message) VALUES (?, ?)", (sender, message))
    conn.commit()
    conn.close()

def get_chatbot_logs(limit=30):
    """
    Gets conversation history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chatbot_logs ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return reversed(rows)

def update_scoring_weights(w_skills, w_exp, w_edu, w_cert, w_proj):
    """
    Updates recruiter configurable scoring weights.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE scoring_weights
        SET skill_weight = ?, experience_weight = ?, education_weight = ?, 
            certification_weight = ?, project_weight = ?
        WHERE id = 1
    ''', (w_skills, w_exp, w_edu, w_cert, w_proj))
    conn.commit()
    conn.close()

def get_scoring_weights():
    """
    Retrieves weights.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scoring_weights WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return {
        "skill_weight": 0.40,
        "experience_weight": 0.25,
        "education_weight": 0.15,
        "certification_weight": 0.10,
        "project_weight": 0.10
    }
