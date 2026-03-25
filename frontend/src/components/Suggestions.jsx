export default function Suggestions({ suggestions }) {
  if (!suggestions || suggestions.length === 0) return null

  // Safety check to ensure we are receiving the new structured objects
  const isStructured = typeof suggestions[0] === 'object'

  return (
    <div className="card" id="suggestions-section">
      <div className="card__title" style={{ borderBottom: '2px solid #eee', paddingBottom: '0.8rem', marginBottom: '1.5rem' }}>
        <span className="card__title-icon">🧠</span>
        Deep Analysis & Coaching
      </div>

      {isStructured ? (
        <div className="suggestions-container">
          {suggestions.map((section, idx) => (
            <div key={idx} className="suggestion-section" style={{ marginBottom: "2rem" }}>
              <h3 style={{ fontSize: "1.2rem", fontWeight: "600", marginBottom: "0.8rem", color: "var(--primary)" }}>
                {section.title}
              </h3>
              <ul className="suggestions-list" style={{ listStyleType: "none", padding: 0, margin: 0 }}>
                {section.items.map((item, i) => (
                  <li key={i} className="suggestion-item" style={{ marginBottom: "0.6rem", fontSize: "1rem", lineHeight: "1.6", color: "#333" }}>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ) : (
        // Fallback for old simple list
        <ul className="suggestions-list">
          {suggestions.map((text, i) => (
            <li key={i} className="suggestion-item">
              <span className="suggestion-item__text">{text}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
