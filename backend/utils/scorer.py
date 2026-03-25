"""
ATS score calculation based on keyword set matching.
"""


def calculate_score(
    resume_keywords: set[str],
    jd_keywords: set[str],
) -> dict:
    """
    Compare resume keywords against job description keywords.

    Returns a dict with:
      - ats_score        (int 0-100)
      - verdict          (str)
      - matched_keywords (sorted list)
      - missing_keywords (sorted list)
      - total_jd_keywords (int)
    """
    if not jd_keywords:
        return {
            "ats_score": 0,
            "verdict": "No job description keywords found",
            "matched_keywords": [],
            "missing_keywords": [],
            "total_jd_keywords": 0,
        }

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    score = round((len(matched) / len(jd_keywords)) * 100)

    # Clamp to 0-100
    score = max(0, min(100, score))

    verdict = _get_verdict(score)

    return {
        "ats_score": score,
        "verdict": verdict,
        "matched_keywords": sorted(matched),
        "missing_keywords": sorted(missing),
        "total_jd_keywords": len(jd_keywords),
    }


def _get_verdict(score: int) -> str:
    """Return a human-readable verdict based on the ATS score."""
    if score >= 80:
        return "Excellent Match 🎯"
    elif score >= 60:
        return "Good Match 👍"
    elif score >= 40:
        return "Fair Match 🔄"
    elif score >= 20:
        return "Weak Match ⚠️"
    else:
        return "Poor Match ❌"
