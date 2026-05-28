import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from dataset_loader import load_or_create_dataset
from parser_engine import ResumeParserModel

app = FastAPI(title="Resume Parser AI API", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize and train model on startup
parser_model = ResumeParserModel()

@app.on_event("startup")
def startup_event():
    print("Loading dataset and training NLP clustering model...")
    df = load_or_create_dataset()
    parser_model.train(df)

class ParseRequest(BaseModel):
    resume_text: str
    target_category: str

class BatchParseRequest(BaseModel):
    resumes: List[Dict[str, str]] # list of dicts with 'name' and 'text'
    target_category: str

@app.get("/api/categories")
def get_categories():
    return {"categories": ["Data Science", "Web Development", "HR", "Sales"]}

@app.post("/api/parse")
def parse_resume(req: ParseRequest):
    if not req.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is empty.")
    
    score_details = parser_model.calculate_score(req.resume_text, req.target_category)
    return score_details

@app.post("/api/parse-batch")
def parse_resumes_batch(req: BatchParseRequest):
    results = []
    for item in req.resumes:
        name = item.get("name", "Unknown Candidate")
        text = item.get("text", "")
        score_details = parser_model.calculate_score(text, req.target_category)
        score_details["name"] = name
        results.append(score_details)
        
    # Sort by score descending to rank candidates
    results.sort(key=lambda x: x.get("score", 0), reverse=True)
    return {"results": results}

@app.get("/api/skills-cluster/{category}")
def get_skills_cluster(category: str):
    if category not in ["Data Science", "Web Development", "HR", "Sales"]:
        raise HTTPException(status_code=400, detail="Invalid job category.")
    return parser_model.get_skill_clusters_visualization(category)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
