"""
FastAPI backend for AI Resume Analyzer (ATS Simulator).
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from utils.parser import extract_text_from_pdf, extract_keywords
from utils.scorer import calculate_score
from utils.suggestions import generate_suggestions

app = FastAPI(
    title="AI Resume Analyzer",
    description="Simulate ATS scoring for resumes against job descriptions.",
    version="1.0.0",
)

# Allow frontend dev server to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API is running 🚀"}

from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd_file: Optional[UploadFile] = File(None),
    job_description: str = Form(""),
):
    """
    Analyze a resume PDF against a job description.
    """
    # 1. Validate the resume
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await resume.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse PDF: {str(e)}")

    # 2. Handle the Job Description (File or Text)
    jd_text = ""
    if jd_file and jd_file.filename.lower().endswith(".pdf"):
        jd_bytes = await jd_file.read()
        try:
            jd_text = extract_text_from_pdf(jd_bytes)
        except:
             pass
    
    if not jd_text.strip():
        jd_text = job_description

    if not jd_text.strip() or not resume_text.strip():
        raise HTTPException(status_code=422, detail="Both Resume and Job description text are required.")

    # 3. Extract keywords and calculate
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    result = calculate_score(resume_keywords, jd_keywords)

    suggestions = generate_suggestions(
        score=result["ats_score"],
        missing_keywords=result["missing_keywords"],
        matched_keywords=result["matched_keywords"],
    )

    return {
        "ats_score": result["ats_score"],
        "verdict": result["verdict"],
        "matched_keywords": result["matched_keywords"],
        "missing_keywords": result["missing_keywords"],
        "total_jd_keywords": result["total_jd_keywords"],
        "suggestions": suggestions,
    }
