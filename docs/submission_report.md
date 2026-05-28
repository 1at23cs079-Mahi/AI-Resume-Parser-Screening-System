# Academic Project Submission Report

## Project Title
**AI Resume Parser and Smart Candidate Screening System (Recruitment Intelligence Platform)**

---

## 1. Abstract
Manual resume screening remains the single most time-consuming constraint in modern corporate talent acquisition. Recruiters spend hours skimming hundreds of candidates for a single open position. Standard Applicant Tracking Systems (ATS) rely on basic literal keyword matching, which fails to capture semantic context (e.g. failing to associate "PyTorch" with "Deep Learning") and are highly vulnerable to candidates gaming the filters via keyword stuffing. 

This project implements a comprehensive **Research-Grade Recruitment Intelligence Platform** that automates candidate screening, domain classification, and ranking. Built using a modular Flask architecture, the system integrates natural language preprocessing (NLTK), supervised machine learning models (Naive Bayes, Logistic Regression, SVM, Random Forest), unsupervised K-Means clustering, and a multi-factor weighted scoring heuristic (0-10) with built-in anti-spam overstuffing penalties and an interactive AI dialog chatbot to answer recruiter queries.

---

## 2. Introduction & Objective
Talent recruitment represents a significant strategic advantage for modern firms. This system applies cognitive computing and machine learning pipelines to solve this challenge. 

### Key Objectives:
1. **Linguistic Normalization:** Convert PDF, DOCX, and scanned text formats into clean, normalized word lemmas.
2. **Cognitive Domain Identification:** Build a supervised learning model to accurately classify candidate backgrounds.
3. **Advanced Semantic Matcher:** Implement Cosine Similarity checks to match candidate experiences against custom job descriptions.
4. **Authenticity Engine:** Verify document formatting and apply repetition penalties to counter keyword overstuffing.
5. **Interactive Recruiter Dashboard:** Enable visual recruitment analytics, dynamic coordinate talent clustering scatter plots, and an intent-driven recruitment chatbot.

---

## 3. Drawbacks of Existing Systems
Traditional keyword-based applicant tracking tools suffer from severe limitations:
- **Zero Semantic Context:** They look for exact strings (e.g. failing to match "Cloud Platform" with "Amazon Web Services").
- **Susceptibility to Spam:** Candidates can copy and paste the entire job description in white text or repeat the word "python" 50 times to force their way to the top of the rankings.
- **Static Scoring:** They offer rigid keyword matching instead of dynamically adjusting weights based on experience, education, or projects.
- **Lack of Explanations:** Recruiters are given a raw score without any contextual feedback on *why* the candidate matched, missing skills, or interview guides.

---

## 4. Methodology & Algorithm Design

### Text Cleaning Pipeline:
$$\text{Resume Unstructured Text} \rightarrow \text{Case-Folding} \rightarrow \text{Punctuation Scrubbing} \rightarrow \text{Word Tokenizer} \rightarrow \text{Stopwords Filter} \rightarrow \text{WordNet Lemmatization}$$

### Dynamic Scoring Function:
The overall candidate score $S$ (out of 10) is calculated as:
$$S = \text{Clamp}_{0}^{10}\left( (S_{\text{skills}} \times W_{\text{skills}}) + (S_{\text{exp}} \times W_{\text{exp}}) + (S_{\text{edu}} \times W_{\text{edu}}) + (S_{\text{cert}} \times W_{\text{cert}}) + (S_{\text{proj}} \times W_{\text{proj}}) - P_{\text{stuffing}} \right)$$
Where $W$ represents configurable recruiter weights, and $P$ represents the keyword stuffing penalty.

---

## 5. Architectural & System Diagrams

### Entity Relationship (ER) Diagram:
```
+------------------------------------+          +--------------------------+
|            CANDIDATES              |          |       CHATBOT_LOGS       |
+------------------------------------+          +--------------------------+
| id (PK)                            |          | id (PK)                  |
| name, email, phone, domain         |          | sender (Text)            |
| text, score, ats_score             |          | message (Text)           |
| raw_breakdown, matched_skills      |          | timestamp (Timestamp)    |
| experience_years, projects_count   |          +--------------------------+
| education, certifications          |
+------------------------------------+
```

### Data Flow Diagram (DFD):
```
[Recruiter] ---> (Upload Resume) ---> (Parsers / OCR) ---> (NLTK Cleaner)
                                                                 |
                                                                 v
[Leaderboard] <--- (Dynamic Weighted Scorer) <--- (ML Classifier & TF-IDF)
```

---

## 6. Future Scope & Conclusion
Future enhancements include:
- Integrating large language models (LLMs) via LangChain for advanced semantic summaries.
- Adding full multi-language parser support.
- Automating direct interview email schedulers.

### Conclusion:
This platform successfully upgrades traditional recruitment pipelines. By implementing semantic skill intelligence, machine learning classifiers, and overstuffing defenses, it provides an authentic, smart, and lightweight ATS suitable for advanced engineering evaluations.
