import os
import json
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

from dataset_loader import load_and_compile_dataset
from preprocessing.text_cleaner import clean_resume_text
from ml_models.vectorizer import TfidfFeatureExtractor

def train_and_evaluate_pipelines():
    """
    Step 4: Model Training.
    Compiles resumes from docx files, fits TF-IDF extractor, splits datasets (80/20),
    trains Naive Bayes, Logistic Regression, SVM, and Random Forest.
    Saves the best model to best_model.pkl and exports confusion matrix metrics.
    """
    print("Beginning Model Training Pipeline...")
    
    # 1. Load Compiled Resumes
    df = load_and_compile_dataset()
    if df.empty or len(df) < 5:
        print("Dataset size is too small for machine learning. Seeding defaults.")
        return
        
    # 2. Clean Text
    print("Preprocessing resume text...")
    df['Cleaned_Resume'] = df['Resume'].apply(lambda x: clean_resume_text(x))
    
    # 3. Feature Extraction
    print("Fitting TF-IDF Vectorizer...")
    extractor = TfidfFeatureExtractor()
    X = extractor.fit_transform(df['Cleaned_Resume'])
    y = df['Category']
    
    # Save fitted vectorizer
    extractor.save_vectorizer('models/tfidf_vectorizer.pkl')
    
    # 4. Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y if y.value_counts().min() > 1 else None
    )
    
    # Declare classifiers
    models = {
        "Naive Bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000, C=1.5),
        "Support Vector Machine (SVM)": SVC(probability=True, kernel='linear'),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    metrics_report = {}
    best_f1 = -1.0
    best_model_name = None
    best_model = None
    
    print("Training classifiers...")
    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            # Compute evaluation statistics
            acc = accuracy_score(y_test, preds)
            prec, rec, f1, _ = precision_recall_fscore_support(y_test, preds, average='weighted', zero_division=0)
            
            # Confusion matrix
            cm = confusion_matrix(y_test, preds)
            
            metrics_report[name] = {
                "accuracy": float(round(acc * 100, 1)),
                "precision": float(round(prec * 100, 1)),
                "recall": float(round(rec * 100, 1)),
                "f1_score": float(round(f1 * 100, 1)),
                "confusion_matrix": cm.tolist()
            }
            
            print(f"-> {name} | Acc: {acc*100:.1f}% | F1: {f1*100:.1f}%")
            
            # Select best model based on weighted F1 score
            if f1 > best_f1:
                best_f1 = f1
                best_model_name = name
                best_model = model
                
        except Exception as e:
            print(f"Error training model {name}: {e}")
            
    # Save the Best Model
    if best_model:
        os.makedirs('models', exist_ok=True)
        with open('models/best_model.pkl', 'wb') as f:
            pickle.dump(best_model, f)
        print(f"Best classifier '{best_model_name}' successfully cached to models/best_model.pkl")
        
        # Save metrics report for visual rendering on the dashboard
        with open('models/metrics.json', 'w') as f:
            json.dump({
                "best_model_name": best_model_name,
                "metrics": metrics_report,
                "unique_labels": list(y.unique())
            }, f, indent=4)
            
if __name__ == '__main__':
    train_and_evaluate_pipelines()
