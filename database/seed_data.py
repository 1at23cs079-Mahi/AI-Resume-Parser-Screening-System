import sqlite3
import json
from database.db_manager import save_candidate, init_db

# Upgraded candidates with identical keys to candidate_ranker.py breakdown structures
SEED_CANDIDATES = [
    {
        "name": "Dr. Sarah Miller",
        "email": "sarah.miller@ai-research.org",
        "phone": "+1 555-010-2345",
        "domain": "Data Science",
        "text": """DR. SARAH MILLER - SENIOR DATA SCIENTIST & ML ARCHITECT
Email: sarah.miller@ai-research.org | Phone: +1 555-010-2345 | GitHub: github.com/sarahm-ml
Professional Summary:
Over 8 years of leading quantitative research teams in developing deep learning classifiers, natural language processing pipelines, and big data clustering algorithms. Highly expert in probability, statistics, and neural network design.

Technical Skills:
- Programming: Python, R, SQL, Julia, Scala
- ML/DL Libraries: TensorFlow, PyTorch, Keras, Scikit-Learn, Pandas, NumPy, SciPy
- Visualization: Matplotlib, Seaborn, Tableau
- Cloud & Big Data: AWS SageMaker, Spark, Hadoop, Databricks, PostgreSQL

Professional Experience:
Lead Machine Learning Engineer | IntellectAI Corp (2021 - Present)
- Architected a custom Transformer-based text preprocessing and classification pipeline, increasing processing accuracy by 32%.
- Trained K-Means clustering algorithms to segment multi-dimensional client behavior profiles over 50 million records.
- Supervised the integration of neural network predictive models on AWS cloud instances.

Education:
- Ph.D. in Computer Science (Specialization: Machine Learning) | Stanford University, 2019.
- M.S. in Mathematical Statistics | MIT, 2015.

Certifications:
- AWS Certified Machine Learning - Specialty, 2023.
- TensorFlow Developer Certificate, 2021.

Projects:
- NeuralStock: Built an LSTM-based recurrent neural network in PyTorch to forecast market fluctuations.
- SemanticQuery: Developed a custom BERT-based semantic search engine over 5 million academic papers.
""",
        "score": 9.4,
        "ats_score": 92.0,
        "breakdown": {
            "skill_relevance": 9.5, 
            "experience_score": 9.8, 
            "education_score": 10.0, 
            "certification_score": 9.0, 
            "project_score": 8.0, 
            "keyword_stuffing_penalty": 0.0
        },
        "matched_skills": {"programming": ["python", "sql", "r"], "libraries": ["pandas", "tensorflow", "pytorch", "scikit-learn"]},
        "skills_list": ["python", "sql", "r", "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "spark", "aws"],
        "source": "Seed File",
        "experience_years": 8.0,
        "projects_count": 4,
        "education": "Ph.D. in Computer Science",
        "certifications": "AWS Machine Learning Specialty, TensorFlow Developer"
    },
    {
        "name": "Clara Oswald",
        "email": "clara.codes@dev.net",
        "phone": "+1 234-567-8910",
        "domain": "Web Development",
        "text": """CLARA OSWALD - LEAD FULL STACK DEVELOPER
Email: clara.codes@dev.net | Phone: +1 234-567-8910 | Portfolio: clara.dev
Summary:
Passionate Web Architect with 6+ years building premium single page applications. Solid expertise in client and server-side state design, relational databases, and secure RESTful microservices.

Core Expertise:
- Languages: JavaScript (ES6+), TypeScript, HTML5, CSS3, SQL
- Frontend: React.js, Next.js, Redux Toolkit, TailwindCSS, Bootstrap, Vite
- Backend: Node.js, Express, FastAPI, Django REST framework
- Databases: PostgreSQL, MongoDB, Redis, Docker virtualization
- CI/CD & Cloud: AWS EC2, Git, GitHub Actions, Jenkins

Projects & Experience:
Senior Web Developer | CloudScale Inc (2021 - Present)
- Architected robust responsive web platforms using React and Vite, achieving a 40% reduction in initial page load speed.
- Developed real-time analytics dashboards using interactive websockets and Node.js backend.
- Managed PostgreSQL databases, optimizing complex relational schemas and query plans.

Education:
- B.S. in Information Technology | University of Washington, 2018.

Certifications:
- AWS Certified Solutions Architect - Associate, 2022.
- Meta Front-End Developer Certificate, 2021.

Projects:
- DevFlow: Developed an open-source collaboration dashboard utilizing React, Redux, and Express.
- SchemaSync: Created a real-time schema migration tool using Node.js and PostgreSQL.
""",
        "score": 8.8,
        "ats_score": 88.0,
        "breakdown": {
            "skill_relevance": 8.9, 
            "experience_score": 9.0, 
            "education_score": 8.0, 
            "certification_score": 8.5, 
            "project_score": 8.0, 
            "keyword_stuffing_penalty": 0.0
        },
        "matched_skills": {"languages": ["javascript", "typescript", "html", "css"], "frontend": ["react", "redux", "tailwind"], "backend": ["node", "express", "fastapi"]},
        "skills_list": ["javascript", "typescript", "html", "css", "react", "redux", "tailwind", "node", "express", "fastapi", "postgresql", "mongodb", "docker", "aws"],
        "source": "Seed File",
        "experience_years": 6.0,
        "projects_count": 3,
        "education": "B.S. in Information Technology",
        "certifications": "AWS Solutions Architect, Meta Front-End Developer"
    },
    {
        "name": "Marcus Aurelius",
        "email": "marcus.sec@cyberdefence.org",
        "phone": "+1 444-987-1111",
        "domain": "Cybersecurity",
        "text": """MARCUS AURELIUS - CYBERSECURITY ANALYST & PENETRATION TESTER
Email: marcus.sec@cyberdefence.org | Phone: +1 444-987-1111
Professional Summary:
CISSP-certified Security Engineer with over 5 years of experience in network penetration testing, vulnerability assessment, threat intelligence, and security operations center (SOC) monitoring.

Technical Skills:
- Security Tools: Wireshark, Metasploit, Nmap, Burp Suite, Kali Linux, Nessus, Snort SIEM
- Protocols: TCP/IP, DNS, SSL/TLS, IPSec, firewalls, routing protocols
- OS: Linux (RedHat, Debian), Windows Server, macOS
- Programming: Python, Bash scripting, PowerShell

Experience:
Senior Information Security Engineer | Aegis Cyber Ltd (2022 - Present)
- Performed weekly network penetration testing and vulnerability assessments for enterprise financial clients.
- Configured Snort IDS rules and Splunk SIEM panels to identify active network breach attempts.
- Conducted staff training on social engineering defense and threat vectors.

Education:
- B.S. in Cybersecurity & Network Administration | University of Maryland, 2020.

Certifications:
- CISSP (Certified Information Systems Security Professional), 2023.
- CEH (Certified Ethical Hacker), 2021.
- CompTIA Security+, 2019.

Projects:
- PortShield: Written a python script utilizing raw sockets to dynamically close vulnerable ports on active port scans.
""",
        "score": 8.5,
        "ats_score": 85.0,
        "breakdown": {
            "skill_relevance": 8.5, 
            "experience_score": 8.5, 
            "education_score": 8.0, 
            "certification_score": 8.5, 
            "project_score": 6.0, 
            "keyword_stuffing_penalty": 0.0
        },
        "matched_skills": {"core": ["pentesting", "vulnerability", "firewalls"], "tools": ["wireshark", "metasploit", "splunk"]},
        "skills_list": ["wireshark", "metasploit", "nmap", "splunk", "python", "bash", "linux", "cissp", "ceh"],
        "source": "Seed File",
        "experience_years": 5.0,
        "projects_count": 2,
        "education": "B.S. in Cybersecurity",
        "certifications": "CISSP, Certified Ethical Hacker (CEH), CompTIA Security+"
    },
    {
        "name": "DevOps David",
        "email": "david.devops@cloudscale.io",
        "phone": "+1 777-888-9999",
        "domain": "DevOps",
        "text": """DAVID MILLER - CLOUD SYSTEMS & DEVOPS ENGINEER
Email: david.devops@cloudscale.io | Phone: +1 777-888-9999 | LinkedIn: linkedin.com/in/david-devops
Summary:
Automation engineer specializing in infrastructure-as-code (IaC), container orchestration, continuous integration pipelines, and AWS cloud management. 

Core Technologies:
- Infrastructure: Terraform, Ansible
- Containerization: Docker, Kubernetes (EKS, GKE)
- CI/CD Tools: Jenkins, GitLab CI, GitHub Actions
- Cloud: AWS, Google Cloud Platform (GCP)
- Scripting: Bash, Python, Go

Professional Experience:
Senior DevOps Engineer | TechSolutions LLC (2022 - Present)
- Migrated legacy microservices into Kubernetes clusters on AWS EKS, reducing cloud spend by 35%.
- Wrote declarative Terraform modules to spin up multi-region VPC environments.
- Implemented robust Jenkins pipeline automating test and deployment configurations, cutting deployment cycles in half.

Education:
- B.S. in Software Engineering | UT Austin, 2019.

Certifications:
- AWS Certified DevOps Engineer - Professional, 2023.
- Certified Kubernetes Administrator (CKA), 2022.

Projects:
- KubeScale: Developed a custom bash utility to scale Kubernetes deployments dynamically based on system metrics.
""",
        "score": 8.9,
        "ats_score": 90.0,
        "breakdown": {
            "skill_relevance": 9.0, 
            "experience_score": 8.8, 
            "education_score": 8.0, 
            "certification_score": 9.0, 
            "project_score": 8.0, 
            "keyword_stuffing_penalty": 0.0
        },
        "matched_skills": {"infrastructure": ["terraform", "ansible"], "containers": ["docker", "kubernetes"], "ci_cd": ["jenkins", "gitlab"]},
        "skills_list": ["terraform", "ansible", "docker", "kubernetes", "jenkins", "git", "bash", "aws", "gcp"],
        "source": "Seed File",
        "experience_years": 4.5,
        "projects_count": 3,
        "education": "B.S. in Software Engineering",
        "certifications": "AWS DevOps Professional, Certified Kubernetes Administrator (CKA)"
    },
    {
        "name": "Keyword Stuffer Spam",
        "email": "spam.candidate@keywordstuffed.com",
        "phone": "+1 000-000-0000",
        "domain": "Data Science",
        "text": """JOHN SPAMMER - DATA SCIENTIST SPECIALIST
Email: spam.candidate@keywordstuffed.com | Phone: +1 000-000-0000
python python python python python python python python python python python python
machine learning machine learning machine learning machine learning machine learning machine learning
TensorFlow TensorFlow TensorFlow TensorFlow TensorFlow TensorFlow TensorFlow TensorFlow
Data Scientist specialized in python, machine learning, deep learning, tensorflow, pytorch, scikit-learn, clustering, sql, pandas, numpy, spark, python.
I do python, python coding, python script, python analysis, tensorflow models, tensorflow deep learning, machine learning frameworks, machine learning, machine learning.
I have certifications in python, tensorflow, machine learning, sql, python, python, python.
""",
        "score": 2.1,
        "ats_score": 15.0,
        "breakdown": {
            "skill_relevance": 6.5, 
            "experience_score": 5.0, 
            "education_score": 5.0, 
            "certification_score": 4.0, 
            "project_score": 2.0, 
            "keyword_stuffing_penalty": 7.5
        },
        "matched_skills": {"programming": ["python", "sql"], "libraries": ["pandas", "tensorflow", "pytorch"]},
        "skills_list": ["python", "sql", "tensorflow", "pytorch", "pandas"],
        "source": "Seed File",
        "experience_years": 0.5,
        "projects_count": 0,
        "education": "Not Specified",
        "certifications": "None"
    }
]

def seed_db():
    """
    Populates tables with high quality candidate resumes.
    """
    init_db()
    
    # Check if candidates exist
    conn = sqlite3.connect('database/recruitment_intelligence.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candidates")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print("Seeding database with professional resume profiles...")
        for c in SEED_CANDIDATES:
            save_candidate(c)
        print(f"Successfully seeded {len(SEED_CANDIDATES)} candidates.")
    else:
        print("Database already contains candidates. Skipping seed.")

if __name__ == '__main__':
    seed_db()
