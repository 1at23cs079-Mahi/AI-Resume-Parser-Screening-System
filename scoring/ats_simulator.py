import re

# Comprehensive list of key sections looked for by standard ATS parsers
MANDATORY_SECTIONS = {
    "Summary/Objective": [r'summary', r'objective', r'profile', r'about\s+me'],
    "Experience": [r'experience', r'employment', r'work\s+history', r'professional\s+background'],
    "Skills": [r'skills', r'core\s+competence', r'expertise', r'technologies'],
    "Education": [r'education', r'academic', r'qualification', r'degree']
}

def analyze_ats_compliance(resume_text: str) -> dict:
    """
    Simulates a standard corporate Applicant Tracking System (ATS) screening.
    Checks section completeness, keyword density, and formatting rules.
    Returns:
      ats_score (0-100), missing_sections, readability, overstuffing_warnings
    """
    text_lower = resume_text.lower()
    total_tokens = len(text_lower.split())
    
    score = 100.0
    deductions = {}
    missing_sections = []
    
    # 1. Section Completeness Check (25 Points Max)
    for section_name, patterns in MANDATORY_SECTIONS.items():
        found = False
        for p in patterns:
            if re.search(r'\b' + p + r'\b', text_lower):
                found = True
                break
        if not found:
            missing_sections.append(section_name)
            score -= 6.0
            deductions[f"Missing Section: {section_name}"] = -6.0
            
    # 2. Contact Info Format Checks (15 Points Max)
    has_email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text_lower)
    has_phone = re.search(r'\+?\d[\d -]{7,12}\d', text_lower)
    has_links = re.search(r'github\.com|linkedin\.com|portfolio', text_lower)
    
    if not has_email:
        score -= 5.0
        deductions["Missing Email Address"] = -5.0
    if not has_phone:
        score -= 5.0
        deductions["Missing Phone Number"] = -5.0
    if not has_links:
        score -= 5.0
        deductions["Missing GitHub/LinkedIn Portfolio Link"] = -5.0
        
    # 3. Readability Index Check (15 Points Max)
    # Simple Coleman-Liau Readability index simulation based on word length
    avg_word_length = 5.0
    if total_tokens > 0:
        words = re.findall(r'[a-zA-Z]+', text_lower)
        if words:
            avg_word_length = sum(len(w) for w in words) / len(words)
            
    readability = "Standard Corporate"
    if avg_word_length > 6.2:
        readability = "Academic/Complex"
        score -= 3.0
        deductions["Complex Readability (Average word length high)"] = -3.0
    elif avg_word_length < 4.0:
        readability = "Very Simple/Informal"
        score -= 4.0
        deductions["Informal Vocabulary / Overly Simple Readability"] = -4.0
        
    # 4. Keyword Density & Artificial Overstuffing Check (30 Points Max)
    # Checks if the same word is repeated too many times
    cleaned_words = re.findall(r'\b[a-zA-Z]{3,}\b', text_lower)
    total_cleaned_words = len(cleaned_words)
    overstuffing_warning = False
    stuffed_keywords = []
    
    if total_cleaned_words > 10:
        from collections import Counter
        counts = Counter(cleaned_words)
        for word, count in counts.items():
            freq = count / total_cleaned_words
            # Keywords repeated consecutively or representing > 6% of resume is a clear ATS gaming attempt
            if freq > 0.06 and count > 3:
                overstuffing_warning = True
                stuffed_keywords.append(word)
                penalty = min((freq - 0.06) * 100.0, 15.0)
                score -= penalty
                deductions[f"Keyword Overstuffing Penalty: '{word}'"] = -round(penalty, 1)
                
    # 5. Format File Layout Validation (15 Points Max)
    # Avoid tables, graphs or unusual symbols
    if re.search(r'[■●★◆▲•|/\\_-]{6,}', text_lower) or text_lower.count('|') > 12:
        score -= 5.0
        deductions["Non-standard Resume Borders or Special Symbols Detected"] = -5.0
        
    score = max(0.0, min(100.0, score))
    
    return {
        "ats_score": round(score, 1),
        "deductions": deductions,
        "missing_sections": missing_sections,
        "readability": readability,
        "stuffed_keywords": stuffed_keywords,
        "overstuffing_warning": overstuffing_warning,
        "recommendations": generate_ats_recommendations(missing_sections, deductions)
    }

def generate_ats_recommendations(missing_sections: list, deductions: dict) -> list:
    """
    Generates actionable bullet points for candidates to improve their ATS score.
    """
    recs = []
    for section in missing_sections:
        recs.append(f"Add a dedicated '{section}' heading to help the parser organize your resume.")
        
    if "Missing Email Address" in deductions or "Missing Phone Number" in deductions:
        recs.append("Ensure your full contact details (email and working telephone number) are clearly placed at the top header.")
        
    if "Missing GitHub/LinkedIn Portfolio Link" in deductions:
        recs.append("Link your GitHub and LinkedIn professional profiles to boost credibility by 5%.")
        
    if any("Overstuffing" in k for k in deductions.keys()):
        recs.append("Reduce the frequency of repetitive terms. Distribute your skills naturally in sentences instead of raw blocks.")
        
    if "Non-standard Resume Borders or Special Symbols Detected" in deductions:
        recs.append("Remove custom horizontal symbols, stars, or vertical divider bars that confuse the line parsers.")
        
    if not recs:
        recs.append("Your resume file layout and semantic density are extremely optimized for modern ATS filters!")
        
    return recs
