import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from config import Config
from security.validator import allowed_file, validate_and_sanitize_filename, sql_injection_check
from database.db_manager import (
    init_db, save_candidate, get_candidates, get_candidate_by_id, 
    save_chatbot_log, get_chatbot_logs, get_scoring_weights, update_scoring_weights
)
from database.seed_data import seed_db
from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from parsers.txt_parser import extract_text_from_txt
from parsers.ocr_parser import extract_text_from_scanned_image
from scoring.scorer import score_candidate, check_duplicate_resume
from scoring.matcher import match_job_description
from ml_models.classifier import DomainClassifierSuite
from clustering.cluster_model import get_resume_clusters
from analytics.dashboard import get_recruiter_kpi_metrics, get_domain_wise_distribution
from chatbot.ai_assistant import process_recruiter_query
from utils.recommender import generate_candidate_recommendations

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Classifier Suite and seed database on startup
classifier_suite = DomainClassifierSuite()

@app.before_request
def startup_checks():
    """
    Performs initial setup, ensures DB is created, seeded, and ML models pre-fit.
    """
    app.before_request_funcs[None].remove(startup_checks)
    print("Pre-training machine learning models and seeding SQLite database...")
    seed_db()
    classifier_suite.train_and_compare()

# Custom Jinja Filter to parse JSON strings inside templates
@app.template_filter('json_loads')
def json_loads_filter(val):
    if not val:
        return {}
    try:
        return json.loads(val)
    except Exception:
        return {}

app.jinja_env.filters['json_loads'] = json_loads_filter
app.jinja_env.globals.update(json_loads=json_loads_filter)

@app.route('/')
def index():
    candidates = get_candidates()
    weights = get_scoring_weights()
    kpis = get_recruiter_kpi_metrics()
    
    # Load default active candidate details if list has profiles
    active_candidate = None
    candidate_id = request.args.get('candidate_id')
    if candidate_id:
        active_candidate = get_candidate_by_id(int(candidate_id))
    elif candidates:
        active_candidate = candidates[0]
        
    recs = None
    if active_candidate:
        recs = generate_candidate_recommendations(dict(active_candidate))
        
    return render_template(
        'dashboard.html', 
        candidates=candidates, 
        active_candidate=active_candidate,
        weights=weights,
        kpis=kpis,
        jd_results=None,
        recs=recs
    )

@app.route('/candidate/<int:cid>')
def view_candidate(cid):
    candidates = get_candidates()
    weights = get_scoring_weights()
    kpis = get_recruiter_kpi_metrics()
    active_candidate = get_candidate_by_id(cid)
    
    recs = None
    if active_candidate:
        recs = generate_candidate_recommendations(dict(active_candidate))
        
    return render_template(
        'dashboard.html', 
        candidates=candidates, 
        active_candidate=active_candidate,
        weights=weights,
        kpis=kpis,
        jd_results=None,
        recs=recs
    )

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return redirect(url_for('index'))
        
    file = request.files['resume']
    target_domain = request.form.get('domain', 'General')
    
    if file.filename == '':
        return redirect(url_for('index'))
        
    if file and allowed_file(file.filename):
        # 1. Sanitize filename
        safe_name = validate_and_sanitize_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        file.save(upload_path)
        
        # 2. Extract Text based on extension
        ext = safe_name.rsplit('.', 1)[1].lower()
        extracted_text = ""
        
        try:
            if ext == 'pdf':
                extracted_text = extract_text_from_pdf(upload_path)
            elif ext == 'docx':
                extracted_text = extract_text_from_docx(upload_path)
            elif ext in ['png', 'jpg', 'jpeg']:
                extracted_text = extract_text_from_scanned_image(upload_path)
            else:
                extracted_text = extract_text_from_txt(upload_path)
                
            if not extracted_text.strip():
                raise ValueError("No text extracted from document.")
                
        except Exception as e:
            # Clean up uploaded file and return error
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return f"Error reading file: {e}", 400
            
        # 3. Check Duplicate
        if check_duplicate_resume(extracted_text):
            if os.path.exists(upload_path):
                os.remove(upload_path)
            return "Error: This candidate resume profile has already been uploaded previously.", 400
            
        # 4. Predict job classification domain
        pred_domain = classifier_suite.predict_domain(extracted_text)
        
        # 5. Dynamic Scorer Assessment
        candidate_data = score_candidate(extracted_text, target_domain)
        candidate_data["domain"] = pred_domain
        candidate_data["source"] = "Upload File"
        
        # 6. Save in SQLite
        cid = save_candidate(candidate_data)
        
        # Clean up file post parsing
        if os.path.exists(upload_path):
            os.remove(upload_path)
            
        return redirect(url_for('index', candidate_id=cid))
        
    return "Invalid file extension.", 400

@app.route('/delete/<int:cid>')
def delete_candidate(cid):
    try:
        conn = sqlite3_connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM candidates WHERE id = ?", (cid,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error deleting candidate {cid}: {e}")
    return redirect(url_for('index'))


@app.route('/match/<int:cid>', methods=['POST'])
def match_jd(cid):
    jd_text = request.form.get('jd', '')
    if sql_injection_check(jd_text):
        return "Security block: Invalid characters or SQL Injection detected in request.", 403
        
    candidate = get_candidate_by_id(cid)
    jd_results = match_job_description(candidate['text'], jd_text)
    
    candidates = get_candidates()
    weights = get_scoring_weights()
    kpis = get_recruiter_kpi_metrics()
    from utils.recommender import generate_candidate_recommendations
    recs = generate_candidate_recommendations(dict(candidate))
    
    return render_template(
        'dashboard.html',
        candidates=candidates,
        active_candidate=candidate,
        weights=weights,
        kpis=kpis,
        jd_results=jd_results,
        jd_text=jd_text,
        recs=recs
    )

@app.route('/weights', methods=['POST'])
def save_weights():
    try:
        w_skills = float(request.form.get('skills', 40)) / 100.0
        w_exp = float(request.form.get('exp', 25)) / 100.0
        w_edu = float(request.form.get('edu', 15)) / 100.0
        
        # Balance certification and projects based on remaining percentage
        rem = max(0.0, 1.0 - (w_skills + w_exp + w_edu))
        w_cert = rem / 2.0
        w_proj = rem / 2.0
        
        update_scoring_weights(w_skills, w_exp, w_edu, w_cert, w_proj)
        
        # Update existing candidate scores dynamically using the new weights
        conn = sqlite3_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, text, domain FROM candidates")
        rows = cursor.fetchall()
        for row in rows:
            c_id, text, dom = row[0], row[1], row[2]
            c_data = score_candidate(text, dom)
            cursor.execute("UPDATE candidates SET score = ?, raw_breakdown = ? WHERE id = ?", (c_data['score'], json.dumps(c_data['breakdown']), c_id))
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error updating weights: {e}")
        
    return redirect(url_for('index'))

@app.route('/analytics')
def analytics():
    domains = get_domain_wise_distribution()
    clusters = get_resume_clusters()
    metrics = classifier_suite.metrics_comparison
    best_model_name = classifier_suite.best_model_name
    
    return render_template(
        'analytics.html',
        domains_json=json.dumps(domains),
        clusters_json=json.dumps(clusters),
        metrics=metrics,
        best_model_name=best_model_name
    )

@app.route('/train', methods=['POST'])
def retrain_models():
    classifier_suite.train_and_compare()
    return redirect(url_for('analytics'))

@app.route('/chatbot')
def chatbot():
    logs = get_chatbot_logs()
    return render_template('chatbot.html', logs=logs)

@app.route('/chatbot/query', methods=['POST'])
def chatbot_query():
    data = request.get_json()
    query = data.get('query', '')
    
    if sql_injection_check(query):
        return jsonify({"response": "Security Warning: Common SQL Injection keywords detected. Query aborted."})
        
    # Save recruiter query
    save_chatbot_log("Recruiter", query)
    
    # Process intent
    response = process_recruiter_query(query)
    
    # Save AI response
    save_chatbot_log("AI", response)
    
    return jsonify({"response": response})

def sqlite3_connect():
    import sqlite3
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    # Initialize DB directories
    init_db()
    app.run(host='127.0.0.1', port=5000, debug=True)
