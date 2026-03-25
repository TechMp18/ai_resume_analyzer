"""
Generate actionable resume improvement suggestions based on ATS analysis.
Returns a structured list of sections for the frontend.
"""

def generate_suggestions(
    score: int,
    missing_keywords: list[str],
    matched_keywords: list[str],
) -> list[dict]:
    
    sections = []

    # --- Section 1: The Honest Truth (Match Analysis) ---
    truth_items = []
    if score >= 80:
        truth_items.append("✅ You are an incredibly strong match for this role. Your keyword foundation is excellent.")
        truth_items.append("👉 Ensure your formatting is clean, metric-driven, and submit!")
    elif score >= 50:
        truth_items.append(f"⚠️ You have a good foundation, but you are still missing {len(missing_keywords)} necessary keywords.")
        truth_items.append("👉 To pass the real ATS, you must weave these missing skills into your 'Work Experience' or 'Projects' sections.")
    else:
        truth_items.append(f"❌ You are missing {len(missing_keywords)} massive keywords that this job expects.")
        truth_items.append("👉 The harsh truth: Without adding the missing core technologies, an ATS will automatically reject this resume.")
    
    sections.append({
        "title": "🧩 1. The Honest Truth (Match Analysis)",
        "items": truth_items
    })

    # --- Section 2: Missing Keywords (CRITICAL for ATS) ---
    missing_items = []
    if missing_keywords:
        top_missing = missing_keywords[:12]  # Just take top 12 to not overwhelm
        missing_items.append("You should add, learn, or mention these core technologies:")
        missing_items.append(f"🔧 Missing Core Skills: {', '.join(top_missing).title()}")
    else:
        missing_items.append("✅ Amazing! You hit all the detected technical keywords. No critical skills missing.")
    
    sections.append({
        "title": "🚨 2. Missing Keywords (CRITICAL for ATS)",
        "items": missing_items
    })

    # --- Section 3: Resume Improvement Suggestions ---
    improvement_items = [
        "🔹 Fix Your SKILLS Section: Don't just list 'Basics'. Group your skills logically (e.g., 'Languages', 'Tools', 'Hardware').",
        "🔹 Upgrade Project Descriptions: Give context. Instead of 'Built a robot', say 'Designed an autonomous robot using C++ and sensor-driven logic'.",
        "🔹 Add IMPACT Words: Replace weak words like 'Worked on' or 'Used' with 'Engineered', 'Architected', or 'Implemented'.",
        "🔹 Quantify Results: ATS algorithms look for numbers! (e.g., 'Reduced latency by 20%' or 'Led a team of 3')."
    ]
    sections.append({
        "title": "✍️ 3. Resume Framing & Wording",
        "items": improvement_items
    })

    return sections
