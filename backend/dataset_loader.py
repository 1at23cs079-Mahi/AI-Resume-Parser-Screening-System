import os
import pandas as pd

# Let's define highly representative resumes for several job categories to build a beautiful training dataset
RESUME_SAMPLES = [
    # Data Science
    ("Data Science", "John Doe - Data Scientist. Highly skilled in Python, Machine Learning, Deep Learning, and Natural Language Processing. Experience with TensorFlow, PyTorch, Scikit-Learn, and Pandas. Created complex clustering models, predictive analytics, and semantic recommendation engines. Proficient in SQL, Jupyter Notebooks, and Big Data technologies like Spark. Strong background in statistics and data visualization using Matplotlib and Seaborn."),
    ("Data Science", "Jane Smith - Machine Learning Engineer. Specializing in Deep Learning, neural networks, and computer vision. Expert in Python, TensorFlow, PyTorch, and Keras. Developed automated classification algorithms and feature engineering pipelines. Worked with large scale datasets, ETL, and model deployment on AWS Cloud. Solid understanding of linear algebra and probability."),
    ("Data Science", "Alex Johnson - Quantitative Research & Data Analyst. Applied statistical modeling and data science to financial markets. Expert in SQL, Python, R, Pandas, NumPy, Scikit-learn. Built predictive regression models, classification trees, and sentiment analysis for news feeds. Experienced with Tableau and data mining."),
    
    # Web Development
    ("Web Development", "David Miller - Senior Frontend Developer. Expert in JavaScript, TypeScript, React.js, and HTML5/CSS3. Proficient in UI/UX principles, CSS frameworks (TailwindCSS, Bootstrap), and state management (Redux, Zustand). Built responsive single page applications, performance optimization, and cross-browser compatibility. Experience with Node.js, Webpack, Vite, and Git version control."),
    ("Web Development", "Emily Davis - Full Stack Engineer. Skilled in frontend and backend development. Stack: React.js, Node.js, Express, MongoDB, PostgreSQL, and JavaScript. Developed RESTful APIs, user authentication, and real-time web sockets. Strong grasp of modern CSS grid, flexbox, and responsive web design. Experienced with Docker and CI/CD pipelines."),
    ("Web Development", "Michael Brown - Backend Developer. Focused on building robust, scalable server side systems. Specialized in Python, Django, FastAPI, PostgreSQL, and Redis. Designed database schemas, optimized SQL queries, and integrated third party APIs. Knowledge of AWS, Docker containers, microservices architecture, and unit testing."),
    
    # HR (Human Resources)
    ("HR", "Sarah Wilson - HR Manager. Expert in talent acquisition, employee relations, recruitment, and onboarding. Proven record in strategic HR planning, performance management, conflict resolution, and HR policies formulation. Proficient with Applicant Tracking Systems (ATS) like Workday and BambooHR. Strong communication and interpersonal skills."),
    ("HR", "James Taylor - Recruitment Specialist. Dedicated to finding top tier talent for technology companies. Experienced in full lifecycle recruitment, candidate sourcing, LinkedIn Recruiter, headhunting, and technical interviews. Managed onboarding, employer branding, and diversity inclusion initiatives."),
    ("HR", "Lisa Anderson - Human Resources Business Partner (HRBP). Strategic partner driving organizational design, employee engagement, leadership coaching, and labor relations. Conducted training programs, performance evaluations, and HR compliance audits. Skilled in employee retention strategies."),
    
    # Sales & Marketing
    ("Sales", "Robert Martin - Sales Executive & Account Manager. Driven to exceed revenue targets and client acquisition goals. Strong negotiation, pipeline management, CRM tools (Salesforce, HubSpot), and cold outreach. Developed strategic sales pitches and managed enterprise B2B sales cycles."),
    ("Sales", "Patricia White - Digital Marketing Manager. Specialized in SEO, SEM, content strategy, and social media advertising (Google Ads, Meta Ads). Analytical approach to conversion rate optimization (CRO) and Google Analytics. Managed email marketing campaigns and brand positioning."),
    ("Sales", "William Thompson - Business Development Representative. Focused on generating qualified leads, market research, and client relationship building. Expert in sales forecasting, customer retention, negotiation, and cross functional team collaboration.")
]

def load_or_create_dataset():
    """
    Ensures that a CSV file containing the resume dataset is available.
    Returns a pandas DataFrame.
    """
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("data", "resumes.csv")
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    
    # Otherwise, write the rich seed samples to CSV
    df = pd.DataFrame(RESUME_SAMPLES, columns=["Category", "Resume"])
    df.to_csv(csv_path, index=False)
    print(f"Dataset created successfully with {len(df)} samples at {csv_path}")
    return df

if __name__ == "__main__":
    load_or_create_dataset()
