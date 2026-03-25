# AI Resume Analyzer (ATS Simulator)

A full-stack web application that simulates how Applicant Tracking Systems (ATS) evaluate resumes against job descriptions.

## Features

- 📊 **ATS Score Calculation** — Score 0–100 based on keyword matching
- 🔍 **Keyword Gap Detection** — Identifies missing skills from the job description
- ✍️ **Improvement Suggestions** — Actionable tips to improve your resume
- 📄 **PDF Upload** — Upload your resume as a PDF
- 🖥️ **Interactive Dashboard** — Beautiful dark-theme results display

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

## Tech Stack

- **Backend:** Python, FastAPI, pdfplumber
- **Frontend:** React (Vite)
- **NLP:** Keyword extraction with set-based matching

## ATS Scoring Logic

```
ATS Score = (Matched Keywords / Total JD Keywords) × 100
```
