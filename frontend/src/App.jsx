import { useState } from 'react'
import ResumeUpload from './components/ResumeUpload.jsx'
import ScoreDisplay from './components/ScoreDisplay.jsx'
import MissingKeywords from './components/MissingKeywords.jsx'
import Suggestions from './components/Suggestions.jsx'

const API_URL = 'http://localhost:8000'

export default function App() {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const canAnalyze = file && jobDescription.trim().length > 10

  const handleAnalyze = async () => {
    if (!canAnalyze) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('resume', file)
      formData.append('job_description', jobDescription)

      const res = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        throw new Error(errData.detail || `Server returned ${res.status}`)
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header__badge">
          <span className="header__badge-dot" />
          ATS Simulator
        </div>
        <h1 className="header__title">AI Resume Analyzer</h1>
        <p className="header__subtitle">
          Upload your resume and paste a job description to get your ATS
          compatibility score with actionable improvement tips.
        </p>
      </header>

      {/* Upload Section */}
      <ResumeUpload
        file={file}
        setFile={setFile}
        jobDescription={jobDescription}
        setJobDescription={setJobDescription}
      />

      {/* Analyze Button */}
      <button
        className="btn-analyze"
        disabled={!canAnalyze || loading}
        onClick={handleAnalyze}
        id="analyze-button"
      >
        {loading ? (
          <>
            <span className="btn-analyze__spinner" />
            Analyzing…
          </>
        ) : (
          <>🚀 Analyze Resume</>
        )}
      </button>

      {/* Error */}
      {error && (
        <div className="error-banner" id="error-banner">
          ⚠️ {error}
        </div>
      )}

      {/* Results Dashboard */}
      {result && (
        <div className="results" id="results-dashboard">
          <div className="results__grid">
            {/* Score Gauge */}
            <ScoreDisplay
              score={result.ats_score}
              verdict={result.verdict}
              matchedCount={result.matched_keywords.length}
              totalKeywords={result.total_jd_keywords}
            />

            {/* Keywords */}
            <MissingKeywords
              missing={result.missing_keywords}
              matched={result.matched_keywords}
            />
          </div>

          {/* Suggestions */}
          <Suggestions suggestions={result.suggestions} />
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        AI Resume Analyzer — Built for learning & demonstration purposes
      </footer>
    </div>
  )
}
