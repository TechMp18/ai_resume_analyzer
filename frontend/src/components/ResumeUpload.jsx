import { useRef, useState } from 'react'

export default function ResumeUpload({ file, setFile, jobDescription, setJobDescription }) {
  const inputRef = useRef(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') setDragActive(true)
    if (e.type === 'dragleave') setDragActive(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    const dropped = e.dataTransfer.files?.[0]
    if (dropped && dropped.name.toLowerCase().endsWith('.pdf')) {
      setFile(dropped)
    }
  }

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0]
    if (selected) setFile(selected)
  }

  return (
    <section className="upload-section" id="upload-section">
      {/* PDF Upload */}
      <div className="card">
        <div className="card__title">
          <span className="card__title-icon">📄</span>
          Upload Resume
        </div>
        <div
          className={`dropzone ${dragActive ? 'dropzone--active' : ''} ${file ? 'dropzone--has-file' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          id="resume-dropzone"
        >
          <span className="dropzone__icon">{file ? '✅' : '📎'}</span>
          {file ? (
            <>
              <p className="dropzone__text">File selected</p>
              <p className="dropzone__filename">{file.name}</p>
            </>
          ) : (
            <>
              <p className="dropzone__text">
                Drag & drop your PDF here, or <strong>click to browse</strong>
              </p>
              <p className="dropzone__hint">Only .pdf files are supported</p>
            </>
          )}
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            className="file-input"
            onChange={handleFileChange}
            id="resume-file-input"
          />
        </div>
      </div>

      {/* Job Description */}
      <div className="card">
        <div className="card__title">
          <span className="card__title-icon">💼</span>
          Job Description
        </div>
        <div className="textarea-wrapper">
          <label className="textarea-label" htmlFor="job-description">
            Paste the job description below
          </label>
          <textarea
            id="job-description"
            className="textarea"
            placeholder="e.g. We are looking for a Full Stack Developer with experience in React, Node.js, Python, Docker, AWS..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>
      </div>
    </section>
  )
}
