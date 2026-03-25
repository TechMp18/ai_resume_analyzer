"""
FastAPI backend for AI Resume Analyzer (ATS Simulator) - Powered by Gemini AI.
"""

from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import json

# 1. Provide the AI with your "Brain" Key
genai.configure(api_key=AIzaSyBspeNXORWxsADEo_ge6AnWNwvziYCqATU)

# Import the basic PDF reader (we still need this to extract the text!)
from utils.parser import extract_text_from_pdf

app = FastAPI(
    title="AI Resume Analyzer",
    description="Simulate ATS scoring for resumes using Google Gemini AI.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API (Gemini Edition) is running 🚀"}

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd_file: Optional[UploadFile] = File(None),
    job_description: str = Form(""),
):
    # 2. Extract texts (Same as before)
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await resume.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        resume_text = extract_text_from_pdf(file_bytes)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse PDF: {str(e)}")

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

    # 3. Call The Brain (Gemini AI)
    # Give the AI clear instructions on how to grade the resume and output JSON
    prompt = f"""
    You are an expert, strict ATS (Applicant Tracking System) and Senior Technical Recruiter.
    Read the following Resume and Job Description.
    
    Resume:
    {resume_text}

    Job Description:
    {jd_text}

    Analyze the resume strictly against the exact technical requirements of the job description.
    Return ONLY a raw JSON object with this EXACT structure (no markdown, no backticks, just the raw JSON text):
    {{
        "ats_score": number (Calculate realistically from 0-100 based strictly on missing skills and experience. Be tough!),
        "verdict": "string (a short verdict like 'Strong Match 🎯', 'Fair Match 🔄', or 'Poor Match ❌')",
        "matched_keywords": ["list", "of", "strings", "(Actual technical skills found in both, like 'Python', 'FPGA', 'React')"],
        "missing_keywords": ["list", "of", "critical", "missing", "skills", "found in JD but missing in Resume"],
        "total_jd_keywords": number (total number of core technical skills found in the JD),
        "suggestions": [
            {{
                "title": "🧩 1. The Honest Truth (Match Analysis)",
                "items": ["Provide direct, brutal feedback on their match specifically for this role based on their actual experience."]
            }},
            {{
                "title": "🚨 2. Missing Keywords (CRITICAL for ATS)",
                "items": ["Focus on the specific hardware/software tools or domain knowledge missing.", "Group them nicely if possible."]
            }},
            {{
                "title": "✍️ 3. Resume Framing & Wording",
                "items": ["Provide extremely specific actionable steps on how to rewrite bullet points for this specific JD based on what they already have."]
            }}
        ]
    }}
    """
    
    try:
        # Ask Google Gemini to do the heavy lifting
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(
            prompt, 
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 4. Parse the beautiful JSON it gives back and send it straight to your Frontend!
        result = json.loads(response.text)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed. Error: {str(e)}")

