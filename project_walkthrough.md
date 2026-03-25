# 🧠 AI Resume Analyzer — Complete Code Walkthrough

This document explains **every file, every function, and every decision** in the project so you actually understand what's happening — not just copy-paste.

---

## 🏗️ The Big Picture

The app has two separate programs talking to each other:

```
┌──────────────┐     HTTP POST      ┌──────────────┐
│   Frontend   │  ──────────────►   │   Backend    │
│  (React app) │                    │  (FastAPI)   │
│  port 5173   │  ◄──────────────   │  port 8000   │
│              │     JSON response  │              │
└──────────────┘                    └──────────────┘
```

- **Frontend** = what the user sees (the dark UI in the browser)
- **Backend** = the "brain" that processes the resume and calculates the score
- They communicate via **HTTP** (same as how your browser talks to any website)

> [!IMPORTANT]
> This is the fundamental architecture of almost every modern web app: a frontend sends requests to a backend API, and gets JSON data back. Understanding this pattern is crucial.

---

## 📦 Backend Deep Dive

### File: [main.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/main.py)

This is the **entry point** of the backend. Let's break it down:

#### What is FastAPI?
FastAPI is a Python framework for building APIs. An **API** (Application Programming Interface) is just a set of URLs that accept data and return data — no web pages, just raw data (JSON).

```python
app = FastAPI(...)  # Creates the application
```

#### What is CORS Middleware?
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)
```
**Problem:** Browsers block requests between different ports by default (port 5173 → port 8000). This is a security feature called "Same-Origin Policy."

**Solution:** CORS (Cross-Origin Resource Sharing) middleware tells the browser: "It's okay, let the frontend talk to me."

> [!TIP]
> `allow_origins=["*"]` means "allow ANY website." In production, you'd restrict this to your actual domain for security.

#### The `/analyze` Endpoint
```python
@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
):
```

- `@app.post("/analyze")` — This creates a URL at `http://localhost:8000/analyze` that only accepts POST requests (POST = sending data)
- `UploadFile = File(...)` — FastAPI automatically handles file uploads
- `str = Form(...)` — This reads the job description text from the form data
- `async` — Allows the server to handle multiple requests simultaneously (doesn't block)

**The flow inside this function:**
```
1. Validate: Is it a .pdf? Is it empty?
2. Extract text from PDF → get raw text
3. Extract keywords from resume text → set of words
4. Extract keywords from job description → set of words
5. Compare the two sets → score + missing keywords
6. Generate suggestions based on the score
7. Return everything as JSON
```

---

### File: [parser.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/utils/parser.py)

This file does TWO things:

#### 1. Extract text from a PDF
```python
def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
```
- `pdfplumber` is a library that reads PDF files and extracts their text
- `BytesIO` wraps raw bytes (from the upload) into a file-like object that pdfplumber can read
- We loop through every page and collect all the text

#### 2. Extract meaningful keywords
```python
def extract_keywords(text: str) -> set[str]:
    text = text.lower()
    tokens = re.findall(r"[a-z][a-z0-9.#+]*[a-z0-9+#]|[a-z]", text)
    # Filter stopwords...
    return keywords
```

**Why a `set`?** A set automatically removes duplicates and allows super-fast lookups (O(1) time complexity). This is KEY for the scoring logic.

**Why stopwords?** Words like "the", "and", "is" appear everywhere and carry no meaning for keyword matching. Removing them gives us only the meaningful technical terms.

**The regex pattern:** `[a-z][a-z0-9.#+]*[a-z0-9+#]` — This matches words like:
- `python`, `react` (normal words)
- `node.js`, `c++`, `c#` (tech terms with special characters)
- `.net` wouldn't match (starts with dot), which is a known limitation

> [!NOTE]
> This is a simplified NLP approach. Real ATS systems use much more advanced techniques like TF-IDF, word embeddings, or transformer models (BERT). But this keyword-based approach is **great for learning** because it's transparent and easy to debug.

---

### File: [scorer.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/utils/scorer.py)

This is the **core algorithm** of the entire project:

```python
matched = resume_keywords & jd_keywords   # Set intersection
missing = jd_keywords - resume_keywords    # Set difference
score = round((len(matched) / len(jd_keywords)) * 100)
```

**Set operations are the hero here:**
- `&` (intersection) = keywords that appear in BOTH resume and JD
- `-` (difference) = keywords in JD but NOT in resume

**Example:**
```
Resume keywords:  {python, react, docker, git, sql}
JD keywords:      {python, react, aws, docker, kubernetes}

Matched (& ):     {python, react, docker}        → 3 keywords
Missing (- ):     {aws, kubernetes}               → 2 keywords
Score:            3/5 × 100 = 60%
Verdict:          "Good Match 👍"
```

> [!TIP]
> This is a real interview-worthy concept. Python sets make complex comparisons trivial. Understanding set operations (`&`, `|`, `-`) is extremely useful in data processing.

---

### File: [suggestions.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/utils/suggestions.py)

This is the simplest file — it's just **conditional logic** that produces different advice based on the score and missing keywords. No fancy algorithm, just practical if/else rules.

```python
if score < 40:
    suggestions.append("Your resume has low keyword overlap...")
if score < 60:
    suggestions.append("Use exact phrases from the job description...")
```

The suggestions get more urgent as the score drops.

---

## 🎨 Frontend Deep Dive

### File: [App.jsx](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/App.jsx)

This is the **main React component** — the "conductor" of the frontend.

#### React State
```javascript
const [file, setFile] = useState(null)          // The uploaded PDF file
const [jobDescription, setJobDescription] = useState('')  // The JD text
const [result, setResult] = useState(null)      // API response data
const [loading, setLoading] = useState(false)   // Is it analyzing?
const [error, setError] = useState('')          // Error message
```

`useState` is React's way of storing data that can change. When you call `setFile(newFile)`, React automatically **re-renders** the parts of the UI that depend on `file`.

#### The API Call
```javascript
const formData = new FormData()
formData.append('resume', file)
formData.append('job_description', jobDescription)

const res = await fetch(`${API_URL}/analyze`, {
  method: 'POST',
  body: formData,
})
```

- `FormData` is the browser API for sending files + text together
- `fetch` sends the HTTP request to our FastAPI backend
- `await` pauses execution until the response comes back
- The names `'resume'` and `'job_description'` must match EXACTLY what FastAPI expects

> [!WARNING]
> A common bug: if the FormData field names don't match the FastAPI parameter names, you'll get a 422 error. This is a frequent interview debugging question.

---

### File: [ScoreDisplay.jsx](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/components/ScoreDisplay.jsx)

The animated circular gauge — this is the most technically interesting component:

```javascript
const CIRCUMFERENCE = 2 * Math.PI * 76  // 2πr, the total length of the circle
const offset = CIRCUMFERENCE - (score / 100) * CIRCUMFERENCE
```

**How the SVG ring works:**
- An SVG circle has a `stroke-dasharray` (total line length) and `stroke-dashoffset` (how much to hide)
- At score 0: offset = full circumference → nothing visible
- At score 100: offset = 0 → full circle visible
- At score 60: 60% of the circle is visible

The counting animation uses `requestAnimationFrame` with an **ease-out cubic** curve:
```javascript
const eased = 1 - Math.pow(1 - progress, 3)
```
This makes the number count fast at first, then slow down — it feels more natural.

---

### File: [index.css](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/index.css)

**CSS Custom Properties (variables):** Everything is defined as `--variable-name` at the top, so changing one value updates the entire app's look.

**Glassmorphism:** The frosted-glass card effect:
```css
background: rgba(17, 24, 39, 0.7);   /* Semi-transparent background */
backdrop-filter: blur(16px);          /* Blur whatever is behind */
border: 1px solid rgba(255,255,255,0.08);  /* Subtle border */
```

**The shimmer animation on the button:**
```css
background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
background-size: 200% 100%;
animation: shimmer 3s ease infinite;
```
This creates a light sweep effect across the button.

---

## 🎯 Concepts You Should Take Away

| Concept | Where It's Used | Why It Matters |
|---|---|---|
| REST API (POST endpoint) | [main.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/main.py) | How frontends talk to backends |
| Set operations | [scorer.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/utils/scorer.py) | Efficient data comparison |
| File upload handling | [main.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/main.py) + [ResumeUpload.jsx](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/components/ResumeUpload.jsx) | Common web app feature |
| React state management | [App.jsx](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/App.jsx) | Core React pattern |
| SVG animation | [ScoreDisplay.jsx](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/components/ScoreDisplay.jsx) | Advanced UI technique |
| CSS custom properties | [index.css](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/frontend/src/index.css) | Scalable design systems |
| CORS | [main.py](file:///c:/Users/mukul/Downloads/Projects/AI%20Resume%20Analyser/backend/main.py) middleware | Web security fundamental |
| Async/await | Both frontend & backend | Modern JavaScript/Python |

---

## 🔮 What Could You Add Next? (Hands-On Learning Ideas)

Here are enhancements **ordered by difficulty** that would teach you new skills:

### 🟢 Easy
1. **Add a "Reset" button** — Clear all results and inputs (practice React state)
2. **Show resume text** — Display the extracted text so users can verify (new component)

### 🟡 Medium
3. **Section-wise scoring** — Score skills, experience, education separately (backend logic)
4. **Export results as PDF** — Generate a downloadable report (learn jsPDF library)
5. **Add charts** — Visualize matched vs missing keywords as a pie/bar chart (learn Chart.js)

### 🔴 Advanced
6. **Semantic similarity with BERT** — Replace keyword matching with AI-powered similarity (learn ML/NLP)
7. **User accounts + history** — Save past analyses using a database (learn MongoDB/SQLite)
8. **Deploy to cloud** — Host on Render/Vercel (learn deployment)

> Pick one from the list above and I'll guide you through building it **step by step** — explaining each concept as we go, not just writing the code for you.
