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
    
    # This is your new ALLOWLISIT. 
    # You can add absolutely any skills you want to this list!
    VALID_SKILLS = {
        # Telecom & Hardware (from your JD)
        "fpga", "vhdl", "verilog", "telecom", "dwdm", "otn", "ptn", "sdn", 
        "mpls", "ethernet", "vlsi", "embedded", "hardware", "board design", 
        "5g", "4g", "lte", "wireless", "wireline", "sonet", "gpon", "iot",

        # Software & Web
        "python", "java", "c++", "c", "c#", "javascript", "typescript", 
        "react", "angular", "node.js", "html", "css", "full stack", 
        "front end", "back end", "rest api", "restful api",

        # Cloud & Data
        "aws", "azure", "gcp", "docker", "kubernetes", "sql", "mysql", 
        "mongodb", "machine learning", "data science", "artificial intelligence", 
        "deep learning", "computer vision", "ci/cd",
        
        # General
        "object oriented", "problem solving", "agile", "scrum"
    }

    keywords = set()
    
    # We simply check if the skill exists anywhere in the messy text
    # This automatically bypasses spacing glitches and ignores normal English words!
    for skill in VALID_SKILLS:
        if skill in text:
            keywords.add(skill)

    return keywords
