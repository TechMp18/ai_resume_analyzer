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


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
    """
    Analyze a resume PDF against a job description.

    - **resume**: PDF file upload
    - **job_description**: Plain-text job description
    """
    # Validate file type
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file.",
        )

    # Read file bytes
    file_bytes = await resume.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Extract text from PDF
    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not parse PDF: {str(e)}",
        )

    if not resume_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract any text from the PDF. "
            "Make sure it is not a scanned image.",
        )

    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_description)

    # Calculate score
    result = calculate_score(resume_keywords, jd_keywords)

    # Generate suggestions
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
