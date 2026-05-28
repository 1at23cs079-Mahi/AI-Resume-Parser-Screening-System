# Resume Parser AI Project

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2F1at23cs079-Mahi%2FAI-Resume-Parser-Screening-System)

---

## 🔗 Project Links

* **GitHub Repository**: [https://github.com/1at23cs079-Mahi/AI-Resume-Parser-Screening-System](https://github.com/1at23cs079-Mahi/AI-Resume-Parser-Screening-System)
* **Live Website**: [https://ai-resume-parser-screening-system.vercel.app/](https://ai-resume-parser-screening-system.vercel.app/)

---

## 1. Project Overview

Recruiters spend a lot of time skimming through resumes to find the best candidate for a job position. Since there can be hundreds of applications for a single position, this process has been automated in several ways as the most common is keyword matching. 

You can build a resume parser with the help of artificial intelligence and machine learning techniques that can skim through a candidate’s application and identify skilled candidates, filtering out people who fill their resume with unnecessary keywords.

### Project Idea

You can use the Resume Dataset available on Kaggle to build this model. This dataset contains only two columns - job title and the candidate’s resume information. The data is present in the form of text and needs to be pre-processed and you can use the NLTK Python library for this data preparation process. 

Then, you can build a clustering algorithm that groups closely related words and skills that a candidate should possess in each domain. Words that are similar in context (and not just keywords) should be considered. You can assign a final weightage score to each resume from 0 (least favourable) to 10 (most favourable). This is the most foundational project if you want to learn AI.

---

## 📂 Project Structure

```text
Resume-Parser-AI-Project/
│
├── .gitignore                   # Excludes local pycaches, environments, and logs from Git
├── .vercelignore                # Excludes heavy datasets and virtualenvs from Vercel uploads
├── requirements.txt             # Python libraries (Flask, NLTK, Scikit-Learn, Pandas, PyPDF, etc.)
├── config.py                    # Configurations (Dynamic SQLite & Upload folders for local/Vercel)
├── app.py                       # Main Flask Server & Route Controller (Chatbot, Analytics, Leaders)
│
├── Launch_Intelligence_Platform.bat  # 1-Click launcher (installs dependencies, seeds DB & runs Flask)
├── vercel.json                  # Serverless function configuration to host Flask instantly on Vercel
│
├── analytics/                   # Recruiter analytics reporting module
│   └── dashboard.py
│
├── chatbot/                     # Dialog AI Recruiter dialogue chatbot agent
│   └── ai_assistant.py
│
├── clustering/                  # Unsupervised K-Means clustering pipelines
│   └── resume_cluster.py
│
├── database/                    # Persistence layer & Pre-populated records
│   ├── db_manager.py            # SQLite database schema, CRUD functions, & cascades deletes
│   ├── seed_data.py             # Preseeded professional resume candidate profiles
│   └── recruitment_intelligence.db # Active SQLite preseeded Database file
│
├── dataset/                     # Core Kaggle Resume Dataset
│   └── resumes.csv
│
├── docs/                        # Academic Submission Documentation & Prep
│   ├── submission_report.md     # Mini-project reports (Objectives, DFD, ER maps, Conclusions)
│   └── viva_questions.md        # Top 25 Viva Voce prep questions & answers
│
├── ml_models/                   # Supervised machine learning algorithms
│   ├── classifier.py            # Comparative training (NB, Logistic Reg, SVM, Random Forest)
│   └── vectorizer.py            # TF-IDF feature extraction pipeline
│
├── models/                      # Saved trained models & metrics
│   ├── best_model.pkl           # Saved best performing trained ML model
│   ├── tfidf_vectorizer.pkl     # Saved fitted TF-IDF vectorizer weights
│   └── metrics.json             # Serialized comparative classifier performance scores
│
├── parsers/                     # Multiformat document readers
│   ├── pdf_parser.py            # Extracts text from PDF candidate resumes
│   ├── docx_parser.py           # Extracts text from DOCX candidate resumes
│   ├── txt_parser.py            # Extracts text from TXT files
│   └── ocr_parser.py            # Scanned resume image OCR text reader fallback
│
├── preprocessing/               # NLP cleaning pipelines (NLTK)
│   ├── text_cleaner.py          # Case-folding, stopwords removal, lemmatization, & sanitization
│   └── cleaner.py
│
├── scoring/                     # ATS and custom suitability scoring engines
│   ├── candidate_ranker.py      # Dynamic weighted scoring algorithm (0 to 10 scale)
│   └── ats_simulator.py         # ATS matching score parser (0 to 100 scale)
│
├── security/                    # Secure validation controls
│   └── validator.py             # File size filters, allowed extensions, and filename sanitizers
│
├── static/                      # Visual Design Sheets
│   └── style.css                # Slate Dark-Theme glassmorphic styling & micro-animations
│
├── templates/                   # User Interfaces (HTML Jinja Templates)
│   ├── dashboard.html           # Main Recruiter Hub & leaderboard panel
│   ├── analytics.html           # 2D PCA K-Means clusters and comparative ML charts page
│   └── chatbot.html             # Conversational AI dialogue interface page
│
├── uploads/                     # Secure server upload location
│   └── .gitkeep                 # Ensures empty directory is tracked on Git clone
│
└── utils/                       # Candidate recommendations engine
    └── recommender.py
```

---

## 2. Setup Instructions

To run the **Resume Parser AI Project** locally on your system, follow these quick and easy steps:

### Prerequisite

Ensure you have Python (version 3.8 or above) installed on your system.

### 🚀 Option A: One-Click Startup (Recommended)

1. Double-click the **`Launch_Intelligence_Platform.bat`** file in the root folder of the project.
2. The batch launcher will automatically:
   * Verify and install all required python dependencies via `pip install -r requirements.txt`.
   * Seed the SQLite database with high-quality candidate records.
   * Load the pre-trained machine learning models and vectorizers.
   * Start the local Flask web server.
   * Open the interactive dashboard in your default browser at `http://127.0.0.1:5000`.

### 🛠️ Option B: Manual Command-Line Setup

1. Open your terminal/command prompt in the project root directory.
2. Install the required python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 3. Usage Steps

Once the website is open, you can easily use all features of the screening platform:
1. **Upload Resumes**: Click the dashed upload dropzone in the sidebar to upload a resume file (PDF, DOCX, or TXT). Select a target domain (e.g. Data Science, Web Development) and click **"Start Cognitive Analysis"**. The system will automatically parse, clean (NLTK), score, and rank the candidate.
2. **Recruiter Weight Adjustments**: Adjust the sliders for Skill Relevance, Experience, Education, Certifications, and Projects in the sidebar to dynamically change candidate suitability scores (0 to 10) in real time.
3. **Semantic Job Description Matching**: Paste any Job Description text in the right-column match panel to compute semantic Cosine Similarity scores.
4. **Conversational AI Assistant**: Click the **"AI Assistant"** tab to talk to the recruitment chatbot. You can ask queries like *"Show top Python candidates"* or *"Suggest interview questions for Sarah Miller"*.
5. **Clustering & Analytics**: Click the **"Analytics & ML"** tab to view the unsupervised K-Means coordinates mapping of candidates (via PCA) and compare evaluation metrics of active ML classifiers.
6. **Delete Candidates**: Select a candidate in the leaderboard queue and click the red trash bin delete button to remove them permanently from the SQLite database.

---

## 4. Supporting Screenshots & Demo Notes

* **Anti-Keyword Stuffing**: Try uploading a resume repeated with the word "Python" multiple times. The system will trigger our custom repetitive-pattern heuristic and penalize the candidate's score heavily (showing spam detection in action).
* **Dynamic Scoring**: Change the "Experience" weight slider to 100% and watch the leaderboard candidate ranking adjust dynamically based solely on candidate experience years.

---

## ⚠️ Important Internship Guidelines

> [!IMPORTANT]
> **Strict Compliance & Authenticity Guidelines:**
> * **Submission Deadline**: Students who fail to submit the mini project within the deadline will not be eligible for further internship progression.
> * **Originality Policy**: Any copied, cheated, or plagiarized work will be strictly rejected. Such students will not be eligible for internship continuation or certificate issuance.
> * **Certificate Issuance**: Certificates will only be issued after successful completion of all required tasks.
