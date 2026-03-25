const ICONS = ['💡', '🎯', '📝', '⚡', '🔑', '📊', '✨', '🚀']

export default function Suggestions({ suggestions }) {
  if (!suggestions || suggestions.length === 0) return null

  return (
    <div className="card" id="suggestions-section">
      <div className="card__title">
        <span className="card__title-icon">✍️</span>
        Improvement Suggestions
      </div>
      <ul className="suggestions-list">
        {suggestions.map((text, i) => (
          <li
            key={i}
            className="suggestion-item"
            style={{ animationDelay: `${i * 0.08}s` }}
          >
            <span className="suggestion-item__icon">
              {ICONS[i % ICONS.length]}
            </span>
            <span className="suggestion-item__text">{text}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
