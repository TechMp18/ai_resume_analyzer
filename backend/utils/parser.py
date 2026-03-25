"""
Resume & Job Description text extraction and keyword parsing utilities.
"""

import re
import pdfplumber
from io import BytesIO

# Common English stopwords to filter out of keyword sets
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "dare", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "just",
    "because", "if", "while", "about", "up", "its", "it", "this", "that",
    "these", "those", "am", "we", "you", "he", "she", "they", "me", "him",
    "her", "us", "them", "my", "your", "his", "our", "their", "what",
    "which", "who", "whom", "i", "able", "also", "etc", "e.g", "per",
    "must", "using", "used", "use", "including", "include", "within",
    "well", "work", "working", "experience", "role", "team", "years",
    "year", "strong", "good", "knowledge", "understanding", "required",
    "preferred", "responsibilities", "requirements", "qualifications",
    "company", "job", "position", "candidate", "looking", "join",
    "opportunity", "description", "minimum", "plus", "equivalent",
}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract all text content from a PDF file."""
    text_parts: list[str] = []
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_keywords(text: str) -> set[str]:
    text = text.lower()

    # 1. Pre-defined multi-word technical skills to look for
    compound_skills = [
        "machine learning", "data science", "full stack", "full-stack",
        "front end", "back end", "node.js", "react native", "react.js",
        "artificial intelligence", "deep learning", "computer vision",
        "natural language processing", "ci/cd", "object oriented", 
        "rest api", "restful api", "problem solving"
    ]
    
    keywords = set()
    
    # Find multi-word skills first, add them, and remove them from the text
    for skill in compound_skills:
        if skill in text:
            keywords.add(skill.replace("-", " ")) # normalize hyphens
            text = text.replace(skill, "")

    # 2. Extract single words
    tokens = re.findall(r"[a-z][a-z0-9.#+]*[a-z0-9+#]|[a-z]", text)

    # 3. Extra words that are NOT skills (we ignore these)
    GENERIC_WORDS = {
        "company", "fast", "paced", "experience", "role", "years", "seeking", 
        "looking", "candidate", "understanding", "knowledge", "required", 
        "preferred", "skills", "ability", "environment", "team", "strong"
    }

    meaningful_single = {"r", "c"}  # Keep R and C programming languages
    
    for token in tokens:
        if token in STOPWORDS or token in GENERIC_WORDS:
            continue
        if len(token) == 1 and token not in meaningful_single:
            continue
        keywords.add(token)

    return keywords
