# Engineering Project Viva Voce & Technical Interview Guide

This guide contains the top 25 technical defense and viva questions with high-scoring answers to help prepare you for your final-year project reviews, external examinations, and internship submissions.

---

## Part 1: Core Natural Language Processing (NLP)

### Q1: What is NLTK and why was it chosen for this project?
**Answer:** NLTK (Natural Language Toolkit) is a leading open-source library in Python for working with human language data. We selected NLTK because it provides highly modular, transparent, and easy-to-customize pipelines for essential pre-processing tasks (tokenization, stopword removal, and lemmatization) without the overhead or large pre-trained weights of libraries like spaCy, ensuring optimal portability on beginner-to-intermediate environments.

### Q2: Explain the differences between Tokenization, Stemming, and Lemmatization.
**Answer:**
*   **Tokenization:** The process of splitting a continuous sequence of text into individual semantic elements called "tokens" (typically words).
*   **Stemming:** A crude heuristic process that chops off the ends of words to reduce them to their base "stem" (e.g., "programming" and "programs" become "program"). It often results in non-dictionary roots.
*   **Lemmatization:** A vocabulary and morphological analysis of words, removing inflectional endings to return the base dictionary form, or "lemma" (e.g., "studying" becomes "study"). It preserves semantic and linguistic accuracy.

### Q3: Why is stopword filtering critical in resume parsing?
**Answer:** Stopwords (e.g., "is", "the", "and", "in") are high-frequency words in human language that carry very little domain-specific semantic meaning. By filtering them out, we dramatically reduce computational noise and dimensionality, letting our machine learning algorithms focus purely on important nouns, technical skills, and tools.

---

## Part 2: Feature Extraction & Classifications

### Q4: How does a TF-IDF Vectorizer work mathematically?
**Answer:** TF-IDF stands for Term Frequency-Inverse Document Frequency. It computes the statistical significance of a word to a document in a collection.
*   **Term Frequency (TF):** Measures how frequently a term $t$ appears in document $d$:
    $$TF(t, d) = \frac{\text{Count of } t \text{ in } d}{\text{Total terms in } d}$$
*   **Inverse Document Frequency (IDF):** Measures how rare the term is across the entire corpus of size $N$:
    $$IDF(t) = \log\left(\frac{N}{1 + \text{Count of documents containing } t}\right)$$
*   **TF-IDF Score:** $TF(t, d) \times IDF(t)$. Words that appear frequently in a single resume but rarely across all resumes (like "TensorFlow") receive high weights, whereas generic words receive low weights.

### Q5: Explain the Naive Bayes Classifier. Why is it called "Naive"?
**Answer:** Naive Bayes is a probabilistic classifier based on Bayes' Theorem:
$$P(C|X) = \frac{P(X|C)P(C)}{P(X)}$$
It is called **"Naive"** because it assumes complete independence between all input features (words) given the class (category), meaning it assumes the presence of the word "Python" has no correlation with the presence of "Pandas". Despite this simplified assumption, it works exceptionally well for text classification.

### Q6: How does a Support Vector Machine (SVM) perform domain classification?
**Answer:** An SVM finds the optimal hyper-plane in a multi-dimensional feature space (spanned by TF-IDF dimensions) that maximizes the margin of separation between different resume categories (e.g., DevOps vs. HR). We use a linear kernel since text representations are highly dimensional and usually linearly separable.

---

## Part 3: Clustering & Dynamic Scoring Heuristics

### Q7: What is the K-Means Clustering Algorithm? How does it segment resumes?
**Answer:** K-Means is an unsupervised machine learning algorithm that groups $N$ data points into $K$ clusters.
1. It initializes $K$ random centroids in the TF-IDF feature space.
2. It assigns each candidate's resume to the nearest centroid using Euclidean distance.
3. It updates centroids by calculating the mean of all data points in that cluster.
4. It repeats this process iteratively until convergence. This segments talent pools dynamically based on term clustering.

### Q8: What is Cosine Similarity and how is it used in Job Description matching?
**Answer:** Cosine similarity measures the cosine of the angle between two multi-dimensional vectors in space. It is calculated as:
$$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
It measures directional alignment (conceptual similarity) rather than vector magnitude (length of resume), making it highly robust. It allows the system to compute a semantic match between a resume and a Job Description.

### Q9: How does the system detect and penalize "Keyword Stuffers"?
**Answer:** Standard Applicant Tracking Systems are vulnerable to candidates repeating key skills to cheat the matching logic. Our **Anti-Keyword Stuffing Engine** computes term frequency counts. If any single term makes up more than 6% of the cleaned tokens (or features exact consecutive repeats like "python python python"), it triggers a stuffing flag, calculates a penalty scaling coefficient, and deducts points from the overall score, pushing spam candidates to the bottom of the list.
