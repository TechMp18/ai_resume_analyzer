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
    """
    Extract meaningful keywords from text.
    - Lowercases everything
    - Keeps only alphanumeric tokens (+ common tech symbols like #, +, .)
    - Removes stopwords and very short tokens
    """
    # Lowercase
    text = text.lower()

    # Tokenize: keep words, and tech terms like c++, c#, .net, node.js
    tokens = re.findall(r"[a-z][a-z0-9.#+]*[a-z0-9+#]|[a-z]", text)

    # Filter stopwords and single-char tokens (except meaningful ones)
    meaningful_single = {"r", "c"}  # programming languages
    keywords = set()
    for token in tokens:
        if token in STOPWORDS:
            continue
        if len(token) == 1 and token not in meaningful_single:
            continue
        keywords.add(token)

    return keywords
