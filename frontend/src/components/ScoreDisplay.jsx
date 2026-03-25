import { useEffect, useState } from 'react'

const CIRCUMFERENCE = 2 * Math.PI * 76 // radius = 76

function getScoreClass(score) {
  if (score >= 80) return 'score--excellent'
  if (score >= 60) return 'score--good'
  if (score >= 40) return 'score--fair'
  if (score >= 20) return 'score--weak'
  return 'score--poor'
}

export default function ScoreDisplay({ score, verdict, matchedCount, totalKeywords }) {
  const [animatedScore, setAnimatedScore] = useState(0)
  const scoreClass = getScoreClass(score)
  const offset = CIRCUMFERENCE - (animatedScore / 100) * CIRCUMFERENCE

  useEffect(() => {
    // Animate the score number counting up
    let start = 0
    const duration = 1200
    const startTime = performance.now()

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      // Ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3)
      const current = Math.round(eased * score)
      setAnimatedScore(current)
      if (progress < 1) requestAnimationFrame(animate)
    }

    requestAnimationFrame(animate)
  }, [score])

  return (
    <div className={`card score-card ${scoreClass}`} id="score-display">
      <div className="score-ring">
        <svg viewBox="0 0 160 160">
          <circle className="score-ring__bg" cx="80" cy="80" r="76" />
          <circle
            className="score-ring__fill"
            cx="80"
            cy="80"
            r="76"
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
          />
        </svg>
        <div className="score-ring__value">
          <span className="score-ring__number">{animatedScore}</span>
          <span className="score-ring__label">ATS Score</span>
        </div>
      </div>
      <div className="score-verdict">{verdict}</div>
      <div className="score-matched">
        {matchedCount} of {totalKeywords} keywords matched
      </div>
    </div>
  )
}
