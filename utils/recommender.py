def generate_candidate_recommendations(candidate_profile: dict) -> dict:
    """
    Generates dynamic suggestions, online courses, active certifications, 
    and resume layout upgrades to elevate the candidate's career.
    """
    domain = candidate_profile.get("domain", "General")
    skills = candidate_profile.get("skills_list", [])
    
    courses = []
    certs = []
    missing_skills = []
    enhancement_tips = []
    
    if domain == "Data Science":
        missing_skills = [s for s in ["PyTorch", "Tableau", "AWS SageMaker", "MLOps", "Spark"] if s.lower() not in [sk.lower() for sk in skills]]
        courses.append("Coursera: Deep Learning Specialization (DeepLearning.AI)")
        courses.append("Udacity: Machine Learning DevOps Engineer Nanodegree")
        certs.append("AWS Certified Machine Learning - Specialty")
        certs.append("Google Cloud Professional Data Engineer")
        enhancement_tips.append("Build a structured 'Projects' section describing multi-node LSTM models or TF-IDF indexing systems.")
        enhancement_tips.append("Link your Kaggle and GitHub repositories clearly at the header profile.")
        
    elif domain == "Web Development":
        missing_skills = [s for s in ["TypeScript", "Next.js", "Docker", "Vite", "GraphQL"] if s.lower() not in [sk.lower() for sk in skills]]
        courses.append("Udemy: Advanced React and Next.js Masterclass")
        courses.append("Coursera: Full-Stack Web Development with React Specialization")
        certs.append("AWS Certified Solutions Architect - Associate")
        certs.append("Meta Certified Lead Front-End Developer")
        enhancement_tips.append("Enrich your experiences by specifying page performance optimization metrics (e.g. 'reduced load speed by 40%').")
        enhancement_tips.append("Add clean GitHub links to open-source collaborations.")
        
    elif domain == "DevOps":
        missing_skills = [s for s in ["Terraform", "Kubernetes", "Ansible", "Jenkins", "AWS"] if s.lower() not in [sk.lower() for sk in skills]]
        courses.append("KodeKloud: Certified Kubernetes Administrator (CKA) Course")
        courses.append("Udemy: Terraform on AWS for Beginners")
        certs.append("Certified Kubernetes Administrator (CKA)")
        certs.append("AWS Certified DevOps Engineer - Professional")
        enhancement_tips.append("Elaborate on Infrastructure as Code (IaC) configuration projects and state management.")
        enhancement_tips.append("List scripting achievements (Bash/Python/Go) demonstrating systems automation.")
        
    else:
        missing_skills = ["System Architecture", "Cloud Integrations", "CI/CD Pipelines", "Containerization"]
        courses.append("Coursera: Google IT Automation with Python Professional Certificate")
        certs.append("CompTIA Security+")
        certs.append("AWS Certified Cloud Practitioner")
        enhancement_tips.append("Structure your resume layout with clear H2 headings: 'Summary', 'Experience', 'Skills', 'Education'.")
        enhancement_tips.append("Detail technical tools utilized under each job entry instead of a single global list.")
        
    return {
        "missing_skills": missing_skills,
        "suggested_courses": courses,
        "recommended_certifications": certs,
        "enhancement_tips": enhancement_tips,
        "suggested_job_roles": [f"Senior {domain} Specialist", f"{domain} Architect", "Information Systems Consultant"]
    }
