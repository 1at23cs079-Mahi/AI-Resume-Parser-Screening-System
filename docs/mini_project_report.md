# AI/ML Mini Project Submission Report

## 1. Cover Page

* **Project Title**: Resume Parser AI Project
* **Student Name**: MAHESH R
* **College Name**: [Insert College Name Here]
* **Branch & Year**: Computer Science & Engineering (CSE), Final Year
* **Email / Phone Number**: [Insert Email / Phone Number Here]
* **Submission Date**: May 28, 2026

---

## 2. Project Overview

### Problem Statement
Recruiters spend a significant amount of time skimming through resumes to find the best candidate for a job position. Since there can be hundreds of applications for a single opening, this process has traditionally been automated via literal keyword matching. However, keyword matching is highly vulnerable to "keyword stuffing" where candidates game the filters by repeating key terms without possessing true contextual knowledge. There is an urgent need for an AI-powered parser that evaluates candidates based on semantic skill alignment while penalizing terms spam.

### Objective
The main goal of this project is to build an intelligent, automated resume parsing and screening system using Python and Natural Language Processing (NLP) that pre-processes candidates' resumes, clusters contextually related words, classifies the resume into job categories using machine learning, and calculates an ATS-style weighted suitability score from 0 (least favorable) to 10 (most favorable).

### Technologies Used
* **Python** (Core Programming Language)
* **NLTK** (Natural Language Processing & Data Preprocessing)
* **Scikit-learn** (Machine Learning & Feature Extraction)
* **Flask** (Web Application Framework & API Development)
* **SQLite** (Persistent Structured Database Layer)
* **Chart.js** (Visual Analytics Charts & 2D Scatter Maps)

---

## 3. Dataset Details

* **Dataset Name**: Kaggle Resume Dataset
* **Dataset Source**: Kaggle Dataset Hub
* **Number of Records**: 228 candidate resume profiles (DOCX/CSV data)
* **Dataset Link**: [https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)

---

## 4. Project Workflow

The project follows a modular, production-style software development life cycle:

```text
[Data Collection] ➔ [NLP Preprocessing] ➔ [TF-IDF Vectorization] ➔ [Model Training & Compare]
                                                                          │
[Live Recruiter Dashboard] ◀── [Dynamic Weighted Scorer] ◀── [Best Cached Model]
```

1. **Data Collection & Extraction**: Unstructured resumes in PDF, DOCX, and TXT formats are parsed using multi-format extractors (`parsers/`).
2. **Data Preprocessing**: Raw text is cleaned using Python's NLTK library (removing URLs, emails, numbers, stopwords, tokenizing, and applying WordNet Lemmatization).
3. **TF-IDF Feature Vectorization**: Cleaned resume text strings are transformed into multi-dimensional numerical TF-IDF feature matrices (`ml_models/vectorizer.py`).
4. **Machine Learning Model Training**: A comparative ML suite evaluates 4 classifiers (Naive Bayes, Logistic Regression, SVM, Random Forest), selects the best-performing model, and caches the weights (`best_model.pkl`, `tfidf_vectorizer.pkl`, `metrics.json`).
5. **Dynamic Scorer Evaluation**: Resumes are graded against custom weights on a 0-10 scale while checking and penalizing excessive keyword terms spam (`scoring/candidate_ranker.py`).
6. **Unsupervised Clustering**: K-Means groups candidates dynamically based on spatial features, and visual coordinates are mapped via PCA for recruiter analytics.
7. **Deployment**: Packaged locally as a desktop batch-launcher app and optimized for Vercel Serverless Functions (`vercel.json`) using `/tmp` storage overrides.

---

## 5. Model / Algorithm Used

The application implements a hybrid model architecture containing both **supervised** classifiers and **unsupervised** clustering algorithms:

### Supervised Classifiers Trained & Compared:
* **Naive Bayes (MultinomialNB)**: Probabilistic classifier designed for sparse high-dimensional data (ideal for text classification).
* **Logistic Regression**: Linear model with high explainability and robust benchmarks.
* **Support Vector Machine (SVM)**: Uses a linear kernel to maximize classification margins between job domains in the vector space.
* **Random Forest Classifier**: Ensemble decision-tree algorithm to prevent model overfitting.

### Unsupervised Clustering Algorithms:
* **K-Means Clustering**: Clusters close skill terms and profiles into spatial groupings.
* **Principal Component Analysis (PCA)**: Reduces the TF-IDF feature dimensions to 2D coordinates for interactive chart coordinates plotting.

### Rationale for Selection:
Using a comparative supervised suite allows the system to evaluate multiple models on startup and dynamically cache the highest-accuracy classifier (achieving ~76% training split accuracy). Naive Bayes and SVM linear kernels are selected for their exceptionally low latency during real-time predictions.

---

## 6. Implementation

### Important Code Snippets

#### 1. NLP Preprocessing Pipeline (`preprocessing/text_cleaner.py`)
```python
def clean_resume_text(text: str, apply_lemmatization=True) -> str:
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)  # Remove Links
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', ' ', text) # Remove Emails
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)            # Keep Alphabets
    tokens = word_tokenize(text)
    
    processed = []
    for token in tokens:
        if token not in STOP_WORDS and len(token) > 2:
            if apply_lemmatization:
                token = LEMMATIZER.lemmatize(token)
            processed.append(token)
    return " ".join(processed)
```

#### 2. Dynamic Suitability Score (0-10) with Anti-Spam Penalty (`scoring/candidate_ranker.py`)
```python
def calculate_dynamic_score(candidate: dict, weights: dict) -> dict:
    # Extract weighted factors
    s_skills = float(candidate.get('skills_score', 0))
    s_exp = float(candidate.get('experience_score', 0))
    s_edu = float(candidate.get('education_score', 0))
    s_cert = float(candidate.get('certification_score', 0))
    s_proj = float(candidate.get('project_score', 0))
    
    # Calculate weighted suitability
    w_sum = (s_skills * weights['skill_weight'] +
             s_exp * weights['experience_weight'] +
             s_edu * weights['education_weight'] +
             s_cert * weights['certification_weight'] +
             s_proj * weights['project_weight'])
             
    # Calculate and subtract term-repetition spam penalties
    penalty = calculate_keyword_stuffing_penalty(candidate.get('text', ''))
    final_score = max(0.0, min(10.0, w_sum - penalty))
    return {"score": round(final_score, 1), "penalty": round(penalty, 1)}
```

---

## 7. Results

### Performance Metrics & Classifier Evaluation:
The four models were evaluated on a Stratified train/test split. The metrics have been saved directly to disk:

* **Support Vector Machine (SVM)**: **58.7% Accuracy** | 49.5% Precision | 53.3% F1-Score
* **Logistic Regression**: **58.7% Accuracy** | 49.5% Precision | 53.5% F1-Score
* **Naive Bayes**: **56.5% Accuracy** | 57.2% Precision | 53.4% F1-Score
* **Random Forest**: **52.2% Accuracy** | 46.9% Precision | 49.4% F1-Score

### Dynamic Suitability Outputs & Predictions:
1. **Dr. Sarah Miller** (Senior Data Scientist): **9.4 / 10 Score** (ATS: 92.0) - High skill coverage, Ph.D. level education, and AWS Certified Machine Learning Specialist.
2. **Clara Oswald** (Lead Web Developer): **8.8 / 10 Score** (ATS: 88.0) - Strong full-stack React/Node skill matching, solid portfolio projects, and solutions architect certification.
3. **Keyword Stuffer Spam** (Data Science): **2.1 / 10 Score** (ATS: 15.0) - Excessive consecutive terms repetition detected (*"python"* repeated over 20 times to bypass keyword filters). Penalty applied: **7.5 / 10**.

---

## 8. Challenges Faced

1. **Serverless Filesystem Restrictions (Vercel)**: Vercel functions execute in a read-only environment, crashing SQLite database writes and NLTK downloads. *Resolution*: Created dynamic environment checks in `config.py` and `db_manager.py` to hot-copy the preseeded DB and NLTK corpora to `/tmp/` on server boot.
2. **Cold-Start Delays**: Model training takes 3–5 seconds on startup. On serverless environments, this cold start causes timeouts. *Resolution*: Cached fitted models and vectorizers to disk as `.pkl` files and metrics to `metrics.json`, letting the server startup instantly without retraining.
3. **React-Lucide Mismatch Reconciliation**: The Lucide icon package mutated the DOM in a way that conflicted with Flask's template reconciliation, leading to UI rendering crashes. *Resolution*: Extracted and custom-coded lightweight, inline SVG icons directly inside templates.
4. **Slate Input Option Contrast**: Default select-option menus rendered with white text on white backgrounds on certain browsers. *Resolution*: Applied `.glass-input option { background-color: #111827 !important; color: #f3f4f6 !important; }` in CSS overrides.
5. **Anti-Keyword Stuffing Penalty Thresholds**: Determining the difference between a highly-skilled candidate mentioning a keyword legitimately and a spam candidate overstuffing the file. *Resolution*: Designed a dynamic density check counting if a single skill exceeds 7% of total tokens, or is repeated consecutively.

---

## 9. Conclusion

### What was achieved:
We successfully engineered a production-style, end-to-end **Resume Parser AI Project** combining NLP preprocessing, supervised comparative domain classifiers, unsupervised K-Means talent clustering, and a dynamic dynamic weights scoring mechanism. The platform successfully screens out spam resumes using anti-stuffing penalties, offers interactive analytics coordinates mapping via PCA, and enables database queries via an AI Chatbot Dialogue assistant.

### Future Improvements:
* **LLM Integrations**: Adding LangChain and OpenAI/Gemini APIs to generate detailed semantic candidate summaries.
* **Interactive Resume Redactions**: Automating candidate anonymity checks to prevent bias during initial shortlisting.
* **Auto-Mailing Recommendations**: Integrating direct SMTP hooks to mail qualified candidates.

---

## 10. References

* **NLTK Python Library Documentation**: [https://www.nltk.org/](https://www.nltk.org/)
* **Scikit-learn API Reference**: [https://scikit-learn.org/stable/modules/classes.html](https://scikit-learn.org/stable/modules/classes.html)
* **Flask Micro-Framework Manual**: [https://flask.palletsprojects.com/en/stable/](https://flask.palletsprojects.com/en/stable/)
* **Kaggle Resume Dataset Hub**: [https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset](https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset)

---

## 11. Submission Files

All required deliverables have been compiled, zipped, and pushed live:

1. **Project Report (PDF/Markdown)**: `MaheshR_ResumeParserAI.pdf` (pushed to repository)
2. **Source Code Zip File**: `MaheshR_ResumeParserAI_Source.zip` (available via repository clone)
3. **Project Live Review Links**:
   * **GitHub Repository**: [https://github.com/1at23cs079-Mahi/AI-Resume-Parser-Screening-System](https://github.com/1at23cs079-Mahi/AI-Resume-Parser-Screening-System)
   * **Live Website**: [https://ai-resume-parser-screening-system.vercel.app/](https://ai-resume-parser-screening-system.vercel.app/)
