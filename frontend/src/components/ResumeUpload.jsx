import { useRef, useState } from 'react'

export default function ResumeUpload({ file, setFile, jdFile, setJdFile, jobDescription, setJobDescription }) {
  const resumeRef = useRef(null)
  const jdRef = useRef(null)
  const [dragActiveResume, setDragActiveResume] = useState(false)
  const [dragActiveJd, setDragActiveJd] = useState(false)

  const handleDrag = (e, type) => {
    e.preventDefault()
    e.stopPropagation()
    const isActive = e.type === 'dragenter' || e.type === 'dragover'
    if (type === 'resume') setDragActiveResume(isActive)
    else setDragActiveJd(isActive)
  }

  const handleDrop = (e, type) => {
    e.preventDefault()
    e.stopPropagation()
    if (type === 'resume') setDragActiveResume(false)
    else setDragActiveJd(false)

    const dropped = e.dataTransfer.files?.[0]
    if (dropped && dropped.name.toLowerCase().endsWith('.pdf')) {
      if (type === 'resume') setFile(dropped)
      else setJdFile(dropped)
    }
  }

  const handleFileChange = (e, type) => {
    const selected = e.target.files?.[0]
    if (selected) {
      if (type === 'resume') setFile(selected)
      else setJdFile(selected)
    }
  }

  return (
    <section className="upload-section" id="upload-section">
      {/* PDF Upload: Resume */}
      <div className="card">
        <div className="card__title"><span className="card__title-icon">📄</span> Upload Resume</div>
        <div
          className={`dropzone ${dragActiveResume ? 'dropzone--active' : ''} ${file ? 'dropzone--has-file' : ''}`}
          onDragEnter={(e) => handleDrag(e, 'resume')}
          onDragOver={(e) => handleDrag(e, 'resume')}
          onDragLeave={(e) => handleDrag(e, 'resume')}
          onDrop={(e) => handleDrop(e, 'resume')}
          onClick={() => resumeRef.current?.click()}
        >
          <span className="dropzone__icon">{file ? '✅' : '📎'}</span>
          {file ? (
            <><p className="dropzone__text">File selected</p><p className="dropzone__filename">{file.name}</p></>
          ) : (
            <><p className="dropzone__text">Drag & drop Resume PDF, or <strong>click to browse</strong></p></>
          )}
          <input ref={resumeRef} type="file" accept=".pdf" className="file-input" onChange={(e) => handleFileChange(e, 'resume')} />
        </div>
      </div>

      {/* PDF Upload: Job Description */}
      <div className="card">
        <div className="card__title"><span className="card__title-icon">💼</span> Job Description</div>

        {/* JD File Dropzone */}
        <div
          className={`dropzone ${dragActiveJd ? 'dropzone--active' : ''} ${jdFile ? 'dropzone--has-file' : ''}`}
          onDragEnter={(e) => handleDrag(e, 'jd')}
          onDragOver={(e) => handleDrag(e, 'jd')}
          onDragLeave={(e) => handleDrag(e, 'jd')}
          onDrop={(e) => handleDrop(e, 'jd')}
          onClick={() => jdRef.current?.click()}
          style={{ marginBottom: '1rem' }}
        >
          <span className="dropzone__icon">{jdFile ? '✅' : '📎'}</span>
          {jdFile ? (
            <><p className="dropzone__text">JD File selected</p><p className="dropzone__filename">{jdFile.name}</p></>
          ) : (
            <><p className="dropzone__text">Drag & drop JD PDF, or <strong>click to browse</strong></p></>
          )}
          <input ref={jdRef} type="file" accept=".pdf" className="file-input" onChange={(e) => handleFileChange(e, 'jd')} />
        </div>

        {/* Fallback Textarea */}
        {!jdFile && (
          <div className="textarea-wrapper">
            <label className="textarea-label" style={{ fontSize: '0.9rem', color: '#666' }}>Or paste text as a fallback:</label>
            <textarea
              className="textarea"
              placeholder="e.g. We are looking for a Full Stack Developer..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
            />
          </div>
        )}
      </div>
    </section>
  )
}
