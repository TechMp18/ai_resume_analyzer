"""
Generate actionable resume improvement suggestions based on ATS analysis.
"""


def generate_suggestions(
    score: int,
    missing_keywords: list[str],
    matched_keywords: list[str],
) -> list[str]:
    """
    Produce a list of actionable suggestions to improve the resume.
    """
    suggestions: list[str] = []

    # --- Missing keywords ---
    if missing_keywords:
        top_missing = missing_keywords[:10]
        suggestions.append(
            f"Add these missing keywords to your resume: "
            f"{', '.join(top_missing)}"
        )

    # --- Score-based advice ---
    if score < 40:
        suggestions.append(
            "Your resume has low keyword overlap with the job description. "
            "Consider tailoring it specifically for this role."
        )
    if score < 60:
        suggestions.append(
            "Use exact phrases and terminology from the job description "
            "rather than synonyms."
        )

    # --- General best practices ---
    suggestions.append(
        "Include measurable achievements (e.g., 'Improved API response "
        "time by 40%') to strengthen your resume."
    )
    suggestions.append(
        "Use strong action verbs like 'developed', 'implemented', "
        "'optimized', 'designed', and 'led'."
    )

    if score < 80:
        suggestions.append(
            "Consider adding a 'Skills' section that explicitly lists "
            "technologies mentioned in the job description."
        )

    if len(matched_keywords) < 5:
        suggestions.append(
            "Your resume matches very few keywords. Try restructuring "
            "your experience to better reflect the required skills."
        )

    suggestions.append(
        "Keep your resume to 1-2 pages and use a clean, ATS-friendly "
        "format (avoid tables, images, and complex layouts)."
    )

    return suggestions
