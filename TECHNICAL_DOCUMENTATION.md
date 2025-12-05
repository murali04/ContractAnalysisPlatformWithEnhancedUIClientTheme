# Contract Analysis Platform - Complete Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Data Flow](#data-flow)
5. [Input Processing](#input-processing)
6. [Semantic Analysis Engine](#semantic-analysis-engine)
7. [Validation Framework](#validation-framework)
8. [Output Generation](#output-generation)
9. [Edge Cases & Error Handling](#edge-cases--error-handling)
10. [Performance Optimization](#performance-optimization)

---

## 1. System Overview

### Purpose
An AI-powered contract compliance analysis platform that validates whether contract clauses satisfy specified obligations using advanced NLP, semantic search, and LLM-based reasoning.

### Key Capabilities
- Multi-format document processing (PDF, DOCX, Excel, CSV, TXT)
- Multi-language support with automatic translation
- Semantic similarity search using vector embeddings
- LLM-powered compliance reasoning
- 7-step validation framework
- Real-time analysis with caching
- Interactive UI with PDF highlighting

---

## 2. Architecture

### High-Level Architecture
```
┌─────────────────┐
│   Frontend      │ (React + TypeScript + Vite)
│   (Port 5173)   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │ (FastAPI + Python)
│   (Port 8000)   │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
│ OpenAI │ │FAISS │ │ spaCy  │ │Translation│
│  API   │ │Vector│ │  NLP   │ │  Service  │
└────────┘ └──────┘ └────────┘ └──────────┘
```

### Component Breakdown

**Frontend Components:**
- `FileUpload.tsx` - File upload interface
- `AnalysisResults.tsx` - Results dashboard
- `ItemsList.tsx` - Obligations list
- `PdfContainer.tsx` - PDF viewer with highlighting
- `TabsPanel.tsx` - Detailed analysis tabs
- `RadialHealthChart.tsx` - Compliance visualization
- `StatusBarChart.tsx` - Status distribution

**Backend Modules:**
- `main.py` - FastAPI application & endpoints
- `core.py` - Core analysis engine
- `core_enhanced.py` - Enhanced features (caching, batching)
- `cache.py` - LRU cache implementation

---

## 3. Technology Stack

### Frontend Stack
```yaml
Framework: React 18.3.1
Language: TypeScript
Build Tool: Vite 6.3.5
Styling: Tailwind CSS 4.1.17
Routing: React Router DOM 7.9.6
Charts: Recharts 2.15.4
Icons: Lucide React 0.555.0
PDF Viewer: @react-pdf-viewer 3.12.0
HTTP Client: Axios 1.13.2
```

### Backend Stack
```yaml
Framework: FastAPI
Language: Python 3.x
LLM: OpenAI GPT-4o-mini
Embeddings: text-embedding-3-small
Vector Store: FAISS (Facebook AI Similarity Search)
NLP: spaCy (en_core_web_sm)
Translation: googletrans + OpenAI fallback
PDF Processing: PyMuPDF (fitz)
Document Processing: python-docx, openpyxl, pandas
Keyword Extraction: KeyBERT
Similarity: scikit-learn (cosine_similarity)
Token Counting: tiktoken
```

---

## 4. Data Flow

### Complete Request-Response Flow

```
1. USER UPLOADS FILES
   ├─ Obligations File (Excel/CSV)
   └─ Contract File (PDF/DOCX/TXT/Excel)
         ↓
2. FRONTEND VALIDATION
   ├─ File type check
   ├─ File size validation
   └─ Format verification
         ↓
3. API REQUEST (POST /api/analyze/enhanced)
   ├─ FormData with files
   └─ Session ID generation
         ↓
4. BACKEND PROCESSING
   ├─ File Reading
   ├─ Language Detection
   ├─ Translation (if needed)
   ├─ Text Extraction
   ├─ Chunking
   ├─ Vector Store Creation
   ├─ Keyword Generation
   ├─ Semantic Search
   ├─ LLM Analysis
   └─ Validation Steps Generation
         ↓
5. RESPONSE GENERATION
   ├─ Results Array
   ├─ Contract URL
   ├─ Full Text
   └─ Cache Statistics
         ↓
6. FRONTEND RENDERING
   ├─ Dashboard Metrics
   ├─ Compliance Charts
   ├─ Obligations List
   ├─ PDF Viewer
   └─ Detailed Analysis Tabs
```

---

## 5. Input Processing

### 5.1 Obligations File Processing

**Supported Formats:** Excel (.xlsx), CSV (.csv)

**Processing Steps:**
```python
# Step 1: Read file
if filename.endswith(".csv"):
    df = pd.read_csv(BytesIO(file_bytes))
else:
    df = pd.read_excel(BytesIO(file_bytes))

# Step 2: Clean columns
df.columns = [str(c).strip() for c in df.columns]

# Step 3: Language detection
df["Language"] = df.iloc[:, 0].apply(detect_language)

# Step 4: Translation to English
df["Obligation_English"] = df.iloc[:, 0].apply(translate_to_english)

# Step 5: Filter empty rows
df = df[df["Obligation_English"].str.strip() != ""]

# Step 6: Extract obligations list
obligations = df["Obligation_English"].tolist()
```

**Example Input:**
```
Obligation
"Vendor must provide 24/7 support"
"All data must be encrypted at rest"
"Vendor shall indemnify customer"
```

**Example Output:**
```python
[
  "Vendor must provide 24/7 support",
  "All data must be encrypted at rest",
  "Vendor shall indemnify customer"
]
```

### 5.2 Contract File Processing

**Supported Formats:** PDF, DOCX, TXT, Excel

#### PDF Processing
```python
def extract_text_from_pdf(file_bytes):
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    records = []
    for page_num, page in enumerate(pdf, start=1):
        lines = page.get_text("text").split("\n")
        for line_num, line in enumerate(lines, start=1):
            if line.strip():
                records.append({
                    "page": page_num,
                    "line": line_num,
                    "text": line.strip()
                })
    return records
```

**Output Structure:**
```python
[
  {"page": 1, "line": 1, "text": "SERVICE LEVEL AGREEMENT"},
  {"page": 1, "line": 2, "text": "Support will be provided during business hours"},
  {"page": 2, "line": 1, "text": "Data encryption using AES-256"}
]
```

#### DOCX Processing
```python
def extract_text_from_docx(file_bytes):
    doc = DocxDocument(BytesIO(file_bytes))
    return [{
        "page": 1,
        "line": i + 1,
        "text": p.text.strip()
    } for i, p in enumerate(doc.paragraphs) if p.text.strip()]
```

### 5.3 Language Detection & Translation

**Detection:**
```python
def detect_language(text):
    lang_code = detect(text)  # Uses langdetect
    flags = {
        "en": "🇬🇧", "es": "🇪🇸", "fr": "🇫🇷",
        "de": "🇩🇪", "it": "🇮🇹", "pt": "🇵🇹"
    }
    return flags.get(lang_code, "🌐")
```

**Translation (Two-tier approach):**
```python
def translate_to_english(text):
    lang_code = detect(text)
    if lang_code != "en":
        try:
            # Primary: Google Translate
            translated = translator.translate(text, src=lang_code, dest="en")
            return translated.text
        except:
            # Fallback: OpenAI
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Translate to English precisely."},
                    {"role": "user", "content": text}
                ]
            )
            return response.choices[0].message.content
    return text
```

**Example:**
- Input (Spanish): "El proveedor debe proporcionar soporte 24/7"
- Output (English): "The vendor must provide 24/7 support"

---

## 6. Semantic Analysis Engine

### 6.1 Text Chunking Strategy

**Purpose:** Break large documents into semantically meaningful chunks for embedding

**Implementation:**
```python
def chunk_text(records):
    # Group by page to maintain context
    pages = {}
    for rec in records:
        page = rec.get("page", 1)
        if page not in pages:
            pages[page] = []
        pages[page].append(rec["text"])
    
    # Use RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,      # Characters per chunk
        chunk_overlap=300     # Overlap for context preservation
    )
    
    docs = []
    for page_num, lines in pages.items():
        page_text = "\n".join(lines)
        chunks = splitter.split_text(page_text)
        
        for idx, chunk in enumerate(chunks):
            docs.append(Document(
                page_content=chunk,
                metadata={"page": page_num, "line": line_num, "chunk_id": idx}
            ))
    
    return docs
```

**Example:**
- Input: 50-page contract (100,000 characters)
- Output: ~70 chunks (1500 chars each, 300 overlap)

### 6.2 Vector Embeddings

**Model:** OpenAI `text-embedding-3-small`
- Dimensions: 1536
- Cost-effective for production
- High semantic accuracy

**Process:**
```python
# Create embeddings
embedder = OpenAIEmbeddings(model="text-embedding-3-small")

# Build FAISS vector store
vs = FAISS.from_documents(docs, embedder)
vs.save_local(vector_path)
```

**Vector Store Structure:**
```
user_memory/
└── faiss_<session_id>_<run_id>/
    ├── index.faiss        # Vector index
    └── index.pkl          # Metadata
```

### 6.3 Dynamic Keyword Generation

**Purpose:** Generate context-aware keywords to enhance retrieval

**LLM-based Generation:**
```python
def generate_dynamic_keywords(obligations):
    keywords_dict = {}
    
    for obligation in obligations:
        # Check cache first
        cache_key = hashlib.sha256(obligation.encode()).hexdigest()
        if cache_key in _keyword_cache:
            keywords_dict[obligation] = _keyword_cache[cache_key]
            continue
        
        # Generate using LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "system",
                "content": "Return 5-8 search terms for the obligation. Predict exact words a vendor would use to LIMIT or AVOID this obligation."
            }, {
                "role": "user",
                "content": obligation
            }],
            temperature=0.0,  # Deterministic
            seed=42,          # Reproducible
            response_format={"type": "json_object"}
        )
        
        keywords = json.loads(response.choices[0].message.content)["keywords"]
        
        # Add universal danger words
        keywords.extend([
            "refund", "reimburse", "terminate", "cap", "limit",
            "sole discretion", "exclusive remedy", "unless", "except"
        ])
        
        keywords = sorted(list(set(keywords)))
        keywords_dict[obligation] = keywords
        
        # Cache for future use
        _keyword_cache[cache_key] = keywords
        save_keyword_cache(_keyword_cache)
    
    return keywords_dict
```

**Example:**
- Obligation: "Vendor must fix all bugs within 24 hours"
- Generated Keywords: ["fix", "repair", "remedy", "bug", "defect", "24 hours", "refund", "reimburse", "terminate", "cap", "limit", "sole discretion"]

### 6.4 Semantic Search (RAG)

**Retrieval Process:**
```python
def query_rag(vs, obligation, auto_keywords, top_k=10):
    # 1. Retrieve top-k similar chunks
    retriever = vs.as_retriever(
        search_type="similarity",
        search_kwargs={"k": top_k}
    )
    docs = retriever.get_relevant_documents(obligation)
    
    # 2. Calculate similarity scores
    ob_emb = embedder.embed_query(obligation)
    doc_embs = [embedder.embed_query(d.page_content) for d in docs]
    sims = cosine_similarity([ob_emb], doc_embs)[0]
    
    # 3. Get best match
    best_idx = np.argmax(sims)
    best_doc = docs[best_idx]
    best_score = float(sims[best_idx])
    
    # 4. Calculate confidence
    confidence = round(best_score * 100, 1)
    
    # 5. Check keyword hits
    keywords = auto_keywords.get(obligation, [])
    keyword_hits = [kw for kw in keywords if kw.lower() in best_doc.page_content.lower()]
    
    return {
        "best_doc": best_doc,
        "similarity_score": best_score,
        "confidence": confidence,
        "keyword_hits": keyword_hits,
        "all_docs": docs
    }
```

**Similarity Calculation:**
```
Cosine Similarity = (A · B) / (||A|| × ||B||)

Where:
- A = Obligation embedding vector (1536 dimensions)
- B = Contract chunk embedding vector (1536 dimensions)
- Result: 0.0 to 1.0 (higher = more similar)
```

**Example:**
- Obligation: "Vendor must provide 24/7 support"
- Top Match: "Support services are available around the clock" (similarity: 0.87)
- Confidence: 87%

---

## 7. Validation Framework

### 7.1 LLM-Powered Compliance Analysis

**Model:** GPT-4o-mini
**Temperature:** 0.0 (deterministic)
**Seed:** 42 (reproducible)
**Max Tokens:** 800

**Prompt Structure:**
```python
prompt = f"""
You are a contract compliance analyst. Analyze whether the contract clause satisfies the obligation.

CRITICAL: Focus on LEGAL EFFECT and COMMERCIAL OUTCOME, not exact wording.

MANDATORY PRE-CHECKS (Check these FIRST):

1. TERMINATION CHECK:
   - IF Obligation requires: "continued use", "ensure access"
   - AND Clause offers: "reimburse", "refund", "credit"
   - THEN Result: "No" (Conflict: Termination ≠ Continued Use)

2. NEGATIVE OBLIGATION CHECK:
   - IF Obligation says: "does NOT have to", "NOT liable"
   - AND Clause has: "unless", "except" conditions
   - AND Conditions RE-IMPOSE the liability
   - THEN Result: "No"

Analysis Framework:
1. Identify the Obligation's Purpose
2. Analyze the Clause's Effect
3. Apply Materiality Test

Return "Yes" if:
- Clause achieves same commercial/legal outcome
- Differences are immaterial
- Alternative methods are acceptable

Return "No" ONLY if:
- Clause negates obligation's core purpose
- Introduces material escape
- Narrows obligation excluding common scenarios

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "Explain the legal effect",
  "suggestion": "If 'No', suggest fix. If 'Yes', return null."
}}

Obligation: {obligation}
Relevant Clauses: {contract_clauses}
"""
```

**Chain-of-Thought Analysis:**
```python
cot_prompt = f"""
{prompt}

IMPORTANT: Think step-by-step:

Step 1: What is the EXACT purpose of the obligation?
Step 2: What does the clause ACTUALLY say?
Step 3: Do they match?
Step 4: Are there any material conflicts?
Step 5: TERMINATION CHECK
Step 6: DISCRETION CHECK
Step 7: NEGATIVE OBLIGATION CHECK

After completing these steps, provide your final JSON answer.
"""
```

**Retry Logic:**
```python
max_retries = 3
retry_delay = 1

for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a meticulous contract compliance expert."},
                {"role": "user", "content": cot_prompt}
            ],
            temperature=0.0,
            seed=42,
            max_tokens=800
        )
        break
    except Exception as e:
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            raise
```

### 7.2 Seven-Step Validation Process

**Step Generation:**
```python
def create_fallback_steps(final_status, reason):
    steps = [
        {"step_number": 1, "step_name": "Identify Obligation Purpose", "status": "PASS"},
        {"step_number": 2, "step_name": "Analyze Clause Effect", "status": "PASS"},
        {"step_number": 3, "step_name": "Match Analysis", "status": "PASS"},
        {"step_number": 4, "step_name": "Material Conflicts Check", "status": "PASS"},
        {"step_number": 5, "step_name": "Termination Check", "status": "PASS", "is_critical": True},
        {"step_number": 6, "step_name": "Discretion Check", "status": "PASS", "is_critical": True},
        {"step_number": 7, "step_name": "Negative Obligation Check", "status": "N/A", "is_critical": True}
    ]
    
    if final_status == "No":
        reason_lower = reason.lower()
        
        # Identify which step failed
        if any(x in reason_lower for x in ["refund", "reimburse", "credit"]):
            steps[4]["status"] = "FAIL"
            steps[4]["finding"] = reason
        elif any(x in reason_lower for x in ["discretion", "sole discretion"]):
            steps[5]["status"] = "FAIL"
            steps[5]["finding"] = reason
        elif any(x in reason_lower for x in ["exception", "unless", "re-impose"]):
            steps[6]["status"] = "FAIL"
            steps[6]["finding"] = reason
        else:
            steps[2]["status"] = "FAIL"
            steps[2]["finding"] = reason
    
    return steps
```

**Validation Steps Explained:**

1. **Identify Obligation Purpose**
   - Extract the core intent
   - Example: "Vendor must fix bugs" → Purpose: Ensure product functionality

2. **Analyze Clause Effect**
   - Determine what the clause actually does
   - Example: "Vendor will repair defects" → Effect: Fixes functionality issues

3. **Match Analysis**
   - Compare purpose vs. effect
   - Example: "Repair defects" matches "fix bugs" ✓

4. **Material Conflicts Check**
   - Identify contradictions
   - Example: "Vendor may fix OR refund" → Conflict if obligation requires fixing

5. **Termination Check** (Critical)
   - Detect termination options when continuity is required
   - Example: Obligation requires "continued use" but clause offers "refund" → FAIL

6. **Discretion Check** (Critical)
   - Distinguish discretion on HOW vs. WHETHER
   - Example: "Vendor chooses method (fix/replace)" = HOW → PASS
   - Example: "Vendor may provide support" = WHETHER → FAIL

7. **Negative Obligation Check** (Critical)
   - Verify exclusions aren't negated by exceptions
   - Example: Obligation: "Not liable for X" + Clause: "Unless Y" → Check if Y re-imposes liability

---

## 8. Output Generation

### 8.1 Response Structure

```typescript
interface AnalysisResult {
  obligation: string;
  is_present: "Yes" | "No";
  reason: string;
  confidence: number;
  similarity_score: number;
  page: number;
  line: number;
  keyword_hits: string[];
  supporting_clauses: string[];
  suggestion: string | null;
  cot_steps: ValidationStep[];
}

interface ValidationStep {
  step_number: number;
  step_name: string;
  status: "PASS" | "FAIL" | "WARNING" | "N/A";
  finding: string;
  is_critical: boolean;
}
```

### 8.2 Example Output

```json
{
  "status": "success",
  "results": [
    {
      "obligation": "Vendor must provide 24/7 support",
      "is_present": "No",
      "reason": "The clause only commits to 'business hours' support, which conflicts with the 24/7 requirement.",
      "confidence": 78.5,
      "similarity_score": 0.785,
      "page": 5,
      "line": 23,
      "keyword_hits": ["support", "hours", "available"],
      "supporting_clauses": [
        "[Page 5 Line 23] Support services will be provided during standard business hours (9 AM - 5 PM EST)"
      ],
      "suggestion": "Add: 'Support services are available 24 hours a day, 7 days a week, including holidays.'",
      "cot_steps": [
        {"step_number": 1, "step_name": "Identify Obligation Purpose", "status": "PASS", "finding": "Obligation requires continuous support availability"},
        {"step_number": 2, "step_name": "Analyze Clause Effect", "status": "PASS", "finding": "Clause provides limited-hours support"},
        {"step_number": 3, "step_name": "Match Analysis", "status": "FAIL", "finding": "Business hours ≠ 24/7 availability"},
        {"step_number": 4, "step_name": "Material Conflicts Check", "status": "FAIL", "finding": "Material difference in availability"},
        {"step_number": 5, "step_name": "Termination Check", "status": "PASS", "finding": "No termination conflicts"},
        {"step_number": 6, "step_name": "Discretion Check", "status": "PASS", "finding": "No problematic discretion"},
        {"step_number": 7, "step_name": "Negative Obligation Check", "status": "N/A", "finding": "Not applicable"}
      ]
    }
  ],
  "contract_url": "/uploads/abc123_contract.pdf",
  "full_text": "...",
  "cache_stats": {
    "hits": 2,
    "misses": 3,
    "hit_rate": 0.4
  }
}
```

### 8.3 CSV Export Format

```csv
Contract Analysis Report
Export Date,2025-12-03T11:30:00Z
Analyzed By,John Doe
Total Obligations,10
Compliant,7
Non-Compliant,3
Compliance Score,70%

Obligation,Status,Reason,Confidence (%),Similarity Score,Page,Line,Suggestion,Supporting Clauses,Validation Steps
"Vendor must provide 24/7 support",No,"Business hours ≠ 24/7",78.5,0.785,5,23,"Add 24/7 availability clause","[Page 5 Line 23] Support during business hours","Step 1: PASS | Step 2: PASS | Step 3: FAIL"
```

---

## 9. Edge Cases & Error Handling

### 9.1 Input Validation Edge Cases

**Empty Files:**
```python
if not obligations or len(obligations) == 0:
    raise HTTPException(status_code=400, detail="No valid obligations found")
```

**Corrupted Files:**
```python
try:
    df = pd.read_excel(BytesIO(file_bytes))
except Exception as e:
    logger.error(f"Failed to read file: {e}")
    raise HTTPException(status_code=400, detail="Invalid file format")
```

**Large Files:**
```python
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
if len(file_bytes) > MAX_FILE_SIZE:
    raise HTTPException(status_code=413, detail="File too large")
```

### 9.2 Translation Edge Cases

**Unsupported Languages:**
```python
try:
    translated = translator.translate(text, src=lang_code, dest="en")
except:
    # Fallback to OpenAI
    translated = openai_translate(text)
```

**Mixed Languages:**
```python
# Process sentence by sentence
sentences = text.split(". ")
translated_sentences = [translate_to_english(s) for s in sentences]
return ". ".join(translated_sentences)
```

### 9.3 Semantic Search Edge Cases

**No Relevant Documents:**
```python
if not docs:
    return {
        "is_present": "No",
        "reason": "No relevant clauses retrieved.",
        "confidence": 0.0,
        "suggestion": "Unable to find relevant clauses in the contract."
    }
```

**Low Similarity Scores:**
```python
if best_score < 0.3:
    logger.warning(f"Low similarity score: {best_score}")
    # Still proceed with LLM analysis for semantic understanding
```

### 9.4 LLM Analysis Edge Cases

**API Failures:**
```python
max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.chat.completions.create(...)
        break
    except Exception as e:
        if attempt == max_retries - 1:
            return {
                "is_present": "No",
                "reason": "Analysis failed due to API error",
                "suggestion": "Please retry the analysis"
            }
        time.sleep(2 ** attempt)  # Exponential backoff
```

**Malformed JSON Responses:**
```python
try:
    parsed = json.loads(response_text)
except json.JSONDecodeError:
    # Try to extract JSON from markdown code blocks
    if "```json" in response_text:
        json_text = response_text.split("```json")[1].split("```")[0]
        parsed = json.loads(json_text)
    else:
        # Fallback
        parsed = {"is_present": "No", "reason": "Could not parse response"}
```

### 9.5 Memory Management

**Vector Store Cleanup:**
```python
@app.on_event("startup")
async def startup_cleanup():
    # Remove old FAISS stores on startup
    for item in os.listdir("user_memory"):
        if item.startswith("faiss_"):
            shutil.rmtree(os.path.join("user_memory", item))

# Cleanup after analysis
try:
    shutil.rmtree(vector_path)
except Exception as e:
    logger.warning(f"Failed to cleanup: {e}")
```

---

## 10. Performance Optimization

### 10.1 Caching Strategy

**Keyword Cache (Persistent):**
```python
# Cache keywords to disk
KEYWORD_CACHE_FILE = "user_memory/keyword_cache/keywords.json"

def load_keyword_cache():
    if os.path.exists(KEYWORD_CACHE_FILE):
        with open(KEYWORD_CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_keyword_cache(cache):
    with open(KEYWORD_CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)
```

**Analysis Results Cache (LRU):**
```python
from functools import lru_cache

class AnalysisCache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get_key(self, obligation, contract_hash):
        return f"{hashlib.sha256(obligation.encode()).hexdigest()}_{contract_hash}"
    
    def get(self, key):
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # Remove oldest entry
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        self.cache[key] = value
```

### 10.2 Batch Processing

**Parallel Analysis:**
```python
from concurrent.futures import ThreadPoolExecutor

def analyze_contract_enhanced(obligations, contract, use_batch=True):
    if use_batch:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(query_rag, vs, ob, keywords)
                for ob in obligations
            ]
            results = [f.result() for f in futures]
    else:
        results = [query_rag(vs, ob, keywords) for ob in obligations]
    
    return results
```

### 10.3 Embedding Optimization

**Model Selection:**
- `text-embedding-3-small`: 1536 dimensions, faster, cost-effective
- `text-embedding-3-large`: 3072 dimensions, more accurate, slower

**Batch Embedding:**
```python
# Instead of one-by-one
embeddings = [embedder.embed_query(text) for text in texts]

# Batch process (if supported)
embeddings = embedder.embed_documents(texts)
```

### 10.4 Performance Metrics

**Typical Performance:**
- File Upload: < 1s
- Text Extraction (50-page PDF): 2-3s
- Vector Store Creation: 3-5s
- Keyword Generation (10 obligations): 5-8s (first time), < 1s (cached)
- Semantic Search per obligation: 0.5-1s
- LLM Analysis per obligation: 2-4s
- Total for 10 obligations: 30-45s (sequential), 15-20s (parallel)

**Optimization Results:**
- Caching: 60-80% faster for repeated obligations
- Batch processing: 40-50% faster for multiple obligations
- Persistent keyword cache: 90% faster on subsequent runs

---

## Appendix: Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-...

# Optional
EMBEDDING_MODEL=text-embedding-3-small  # or text-embedding-3-large
USE_CACHE=true
BATCH_SIZE=5
LOG_LEVEL=INFO
```

### File Structure
```
ContractAnalysisPlatformGuardRails/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── core.py              # Core analysis
│   ├── core_enhanced.py     # Enhanced features
│   ├── cache.py             # Caching logic
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── charts/          # Chart components
│   │   └── context/         # Auth context
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite config
├── uploads/                 # Uploaded files
├── user_memory/             # Vector stores & cache
│   └── keyword_cache/       # Persistent keywords
├── .env                     # Environment variables
└── README.md                # Documentation
```

---

**Document Version:** 1.0  
**Last Updated:** 2025-12-03  
**Author:** Technical Documentation Team
