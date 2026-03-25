export default function MissingKeywords({ missing, matched }) {
  return (
    <div className="card keywords-section" id="keywords-section">
      <div className="card__title">
        <span className="card__title-icon">🔍</span>
        Keyword Analysis
      </div>

      {/* Missing Keywords */}
      {missing.length > 0 && (
        <div>
          <div className="keywords-group__label">
            ❌ Missing Keywords
            <span className="keywords-group__count">{missing.length}</span>
          </div>
          <div className="keyword-tags">
            {missing.map((kw, i) => (
              <span
                key={kw}
                className="keyword-tag keyword-tag--missing"
                style={{ animationDelay: `${i * 0.04}s` }}
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Matched Keywords */}
      {matched.length > 0 && (
        <div>
          <div className="keywords-group__label">
            ✅ Matched Keywords
            <span className="keywords-group__count">{matched.length}</span>
          </div>
          <div className="keyword-tags">
            {matched.map((kw, i) => (
              <span
                key={kw}
                className="keyword-tag keyword-tag--matched"
                style={{ animationDelay: `${i * 0.04}s` }}
              >
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
