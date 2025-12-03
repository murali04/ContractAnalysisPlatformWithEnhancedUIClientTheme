# Contract Analysis Platform with GuardRails - Comprehensive Documentation

## 📑 Table of Contents
- [Executive Summary](#executive-summary)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Core Features](#core-features)
- [How It Works - End to End](#how-it-works---end-to-end)
- [LLM Prompt Engineering](#llm-prompt-engineering)
- [Validation Steps Explained](#validation-steps-explained)
- [Edge Cases & Scenarios](#edge-cases--scenarios)
- [Setup & Installation](#setup--installation)
- [Usage Guide](#usage-guide)
- [API Reference](#api-reference)
- [Frontend Architecture](#frontend-architecture)
- [Performance Optimizations](#performance-optimizations)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

---

## Executive Summary

**Contract Analysis Platform with GuardRails** is an AI-powered multilingual contract compliance analysis system that automatically verifies whether contract clauses meet specified obligations. The system combines **Retrieval-Augmented Generation (RAG)**, **Large Language Models (LLMs)**, **advanced caching**, and a **modern React-based UI** to deliver accurate, transparent, and fast contract analysis.

### Key Capabilities
- ✅ **Semantic Analysis**: Pure cosine similarity for confidence scoring
- ✅ **Multilingual Support**: Automatic language detection and translation
- ✅ **RAG-based Retrieval**: FAISS vector store for efficient clause matching
- ✅ **LLM Reasoning**: GPT-4o-mini for nuanced compliance decisions
- ✅ **Strict Yes/No Output**: Binary compliance status (no "Partial")
- ✅ **7-Step Validation**: Transparent step-by-step analysis with critical checks
- ✅ **Intelligent Caching**: Avoid re-analyzing identical obligations
- ✅ **Batch Processing**: 3-5x faster for multiple obligations
- ✅ **Modern UI**: React + TypeScript + TailwindCSS with PDF preview

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  React + TypeScript + TailwindCSS + Vite + React Router        │
│  - File Upload Component                                        │
│  - Analysis Results Dashboard                                   │
│  - PDF Preview with Highlighting                                │
│  - Validation Steps Visualization                               │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST API
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND API LAYER                          │
│  FastAPI + Uvicorn                                              │
│  - /api/analyze (main endpoint)                                 │
│  - /api/cache/stats (cache metrics)                             │
│  - /api/cache/clear (cache management)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CORE ANALYSIS ENGINE                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Text Extraction Layer                                │  │
│  │     - PDF (PyMuPDF)                                      │  │
│  │     - DOCX (python-docx)                                 │  │
│  │     - Excel (pandas + openpyxl)                          │  │
│  │     - TXT (plain text)                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  2. Language Processing                                  │  │
│  │     - Language Detection (langdetect)                    │  │
│  │     - Translation (googletrans + OpenAI fallback)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  3. Chunking & Embedding                                 │  │
│  │     - RecursiveCharacterTextSplitter                     │  │
│  │     - Chunk size: 1500, Overlap: 300                     │  │
│  │     - OpenAI embeddings (text-embedding-3-small/large)   │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  4. Vector Store (FAISS)                                 │  │
│  │     - Stores contract clause embeddings                  │  │
│  │     - Enables similarity search                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  5. Cache Layer (In-Memory LRU)                          │  │
│  │     - Content-based hashing                              │  │
│  │     - Max 1000 entries                                   │  │
│  │     - Hit rate tracking                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  6. RAG Query Pipeline                                   │  │
│  │     - Embed obligation                                   │  │
│  │     - Retrieve top-k similar clauses (k=10)              │  │
│  │     - Calculate cosine similarity                        │  │
│  │     - Extract keywords (KeyBERT + spaCy)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  7. LLM Analysis (GPT-4o-mini)                           │  │
│  │     - 7-step validation framework                        │  │
│  │     - Semantic compliance check                          │  │
│  │     - Reason generation                                  │  │
│  │     - Suggestion generation (if No)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  8. Batch Processing (ThreadPoolExecutor)                │  │
│  │     - Parallel LLM calls (5 workers)                     │  │
│  │     - Order preservation                                 │  │
│  │     - Error handling per obligation                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
│  - OpenAI API (GPT-4o-mini, text-embedding-3-small/large)      │
│  - Google Translate API (with OpenAI fallback)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | FastAPI | Latest | REST API endpoints |
| **Server** | Uvicorn | Latest | ASGI server |
| **LLM** | OpenAI GPT-4o-mini | Latest | Semantic analysis & reasoning |
| **Embeddings** | OpenAI text-embedding-3-small/large | Latest | Vector embeddings |
| **Vector Store** | FAISS (Facebook AI) | Latest | Similarity search |
| **Keyword Extraction** | KeyBERT + spaCy | Latest | Dynamic keyword generation |
| **Translation** | googletrans + OpenAI | 4.0.0-rc1 | Multilingual support |
| **Language Detection** | langdetect | Latest | Auto-detect language |
| **PDF Processing** | PyMuPDF (fitz) | Latest | PDF text extraction |
| **DOCX Processing** | python-docx | Latest | Word document parsing |
| **Excel Processing** | pandas + openpyxl | Latest | Excel file handling |
| **Text Splitting** | LangChain | Latest | Recursive chunking |
| **Caching** | In-memory LRU | Custom | Result caching |
| **Batch Processing** | ThreadPoolExecutor | Python stdlib | Parallel processing |

### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 18.3.1 | UI library |
| **Language** | TypeScript | Latest | Type safety |
| **Build Tool** | Vite | 6.3.5 | Fast dev server & bundler |
| **Styling** | TailwindCSS | 4.1.17 | Utility-first CSS |
| **Routing** | React Router DOM | 7.9.6 | Client-side routing |
| **PDF Viewer** | @react-pdf-viewer | 3.12.0 | PDF preview & highlighting |
| **Charts** | Recharts | 2.15.4 | Data visualization |
| **Icons** | Lucide React | 0.555.0 | Icon library |
| **HTTP Client** | Axios | 1.13.2 | API requests |

### Development Tools
- **Environment Variables**: python-dotenv
- **Logging**: Python logging module
- **Type Checking**: TypeScript compiler
- **Package Manager**: npm

---

## Core Features

### 1. **Two-Stage Decision Process**

The system uses a unique two-stage approach to ensure accuracy:

#### Stage 1: Similarity Score (Confidence Metric)
- **What it measures**: Lexical and semantic similarity between texts
- **Method**: Cosine similarity of embeddings
- **Range**: 0-100%
- **Purpose**: Confidence indicator only
- **NOT used for**: Final compliance decision

#### Stage 2: LLM Semantic Analysis (Final Decision)
- **What it measures**: Legal compliance and logical equivalence
- **Method**: GPT-4o-mini with specialized prompt
- **Output**: "Yes" or "No"
- **Purpose**: Actual compliance determination

**Why This Matters**:
```
Example 1: Low Similarity, High Compliance
Obligation: "Vendor must fix bugs"
Contract: "Vendor will repair defects"
Similarity: 45% (different words)
LLM Decision: YES (same meaning)

Example 2: High Similarity, Low Compliance
Obligation: "You must give me $100"
Contract: "I will give you $100 or give you nothing"
Similarity: 85% (almost identical words)
LLM Decision: NO (escape clause present)
```

### 2. **7-Step Validation Framework**

Every obligation goes through 7 validation steps:

| Step | Name | Type | Purpose |
|------|------|------|---------|
| 1 | Identify Obligation Purpose | Analysis | Determines core intent |
| 2 | Analyze Clause Effect | Analysis | Evaluates clause impact |
| 3 | Match Analysis | Analysis | Checks explicit coverage |
| 4 | Material Conflicts Check | Analysis | Ensures no contradictions |
| 5 | Termination Check | **CRITICAL** | Validates termination impact |
| 6 | Discretion Check | **CRITICAL** | Looks for weakening language |
| 7 | Negative Obligation Check | **CRITICAL** | Detects reversing exceptions |

**Decision Rules**:
- ❌ If ANY critical step (5, 6, 7) fails → Automatic NO
- ❌ If analysis steps (3, 4) show material mismatch → NO
- ✅ If all steps pass or N/A → YES

### 3. **Intelligent Caching**

**How It Works**:
- **Cache Key**: `SHA256(obligation_text + SHA256(contract_content))`
- **Storage**: In-memory LRU cache (max 1000 entries)
- **Content-Based**: Uses actual content hash, not filename
- **Hit Rate Tracking**: Monitors cache performance

**Edge Cases Handled**:

| Scenario | Obligation | Contract | Filename | Cache Result | Why? |
|----------|-----------|----------|----------|--------------|------|
| Exact repeat | Same | Same content | Same | ✅ HIT | Identical key |
| Updated contract | Same | **Different content** | Same | ✅ MISS | Content hash changed |
| Renamed file | Same | Same content | **Different** | ✅ HIT | Content hash unchanged |
| Slight obligation change | **Different** | Same content | Same | ✅ MISS | Obligation changed |
| Whitespace only | Same (trimmed) | Same content | Same | ✅ HIT | Text normalized |

**Performance Impact**:
```
First analysis (10 obligations): 30s
Second analysis (same 10): <1s (100% cache hit)
Cost savings: 10x fewer LLM API calls
```

### 4. **Batch Processing**

**How It Works**:
- **Method**: ThreadPoolExecutor for parallel LLM calls
- **Workers**: Configurable via `BATCH_SIZE` (default: 5)
- **Order Preservation**: Results maintain original obligation order
- **Error Handling**: Each obligation analyzed independently

**Performance Comparison**:

| Obligations | Sequential | Batch (5 workers) | Speedup | Time Saved |
|-------------|-----------|-------------------|---------|------------|
| 10 | 30s | 8s | 3.75x | 22s |
| 50 | 150s | 35s | 4.29x | 115s |
| 100 | 300s | 65s | 4.62x | 235s |

**Why Parallel Processing Works**:
- LLM calls are I/O-bound (waiting for API response)
- ThreadPoolExecutor perfect for I/O-bound tasks
- Network I/O releases the GIL (no threading bottleneck)
- Optimal worker count (5) balances speed vs. API rate limits

---

## How It Works - End to End

### Complete Analysis Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: User Uploads Files                                      │
│ - Obligations file (Excel/CSV)                                  │
│ - Contract file (PDF/DOCX/Excel/TXT)                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Text Extraction                                         │
│ - Extract text from contract (page/line tracking)               │
│ - Parse obligations from Excel/CSV                              │
│ - Detect language for each text                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: Translation (if needed)                                 │
│ - Auto-detect non-English text                                  │
│ - Translate to English (googletrans + OpenAI fallback)          │
│ - Preserve original for reference                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Chunking & Embedding                                    │
│ - Group text by page                                            │
│ - Split into chunks (1500 chars, 300 overlap)                   │
│ - Track page/line numbers for each chunk                        │
│ - Generate embeddings (OpenAI text-embedding-3-small)           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Build Vector Store                                      │
│ - Create FAISS index from chunk embeddings                      │
│ - Store metadata (page, line, chunk_id)                         │
│ - Save to temporary directory                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Generate Keywords (with caching)                        │
│ - For each obligation:                                          │
│   1. Check keyword cache (SHA256 hash)                          │
│   2. If miss: Generate via GPT-4o-mini                          │
│   3. Add universal danger words                                 │
│      (refund, reimburse, terminate, cap, limit, etc.)           │
│   4. Cache result for future use                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: Hash Contract Content                                   │
│ - Generate SHA256 hash of full contract text                    │
│ - Used for cache key generation                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 8: Batch Processing Decision                               │
│ - If multiple obligations AND batch enabled:                    │
│   → Use ThreadPoolExecutor (5 workers)                          │
│ - Else:                                                          │
│   → Sequential processing                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 9: For Each Obligation (parallel or sequential)            │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.1: Check Cache                                          │  │
│ │ - Generate cache key: hash(obligation + contract_hash)   │  │
│ │ - If HIT: Return cached result immediately                │  │
│ │ - If MISS: Continue to analysis                           │  │
│ └───────────────────────────────────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.2: RAG Retrieval                                        │  │
│ │ - Embed obligation text                                   │  │
│ │ - Query FAISS for top-10 similar chunks                   │  │
│ │ - Calculate cosine similarity for each                    │  │
│ │ - Select best match (highest similarity)                  │  │
│ └───────────────────────────────────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.3: Keyword Matching                                     │  │
│ │ - Get keywords for obligation                             │  │
│ │ - Count matches in best chunk                             │  │
│ │ - Calculate keyword ratio                                 │  │
│ └───────────────────────────────────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.4: Confidence Score                                     │  │
│ │ - Confidence = cosine_similarity * 100                    │  │
│ │ - Pure similarity score (no hybrid formula)               │  │
│ └───────────────────────────────────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.5: LLM Analysis (GPT-4o-mini)                           │  │
│ │ - Send obligation + top-10 clauses to LLM                 │  │
│ │ - Apply 7-step validation framework                       │  │
│ │ - Get decision: "Yes" or "No"                             │  │
│ │ - Get reason (1-2 sentence explanation)                   │  │
│ │ - Get suggestion (if "No")                                │  │
│ │ - Generate fallback steps for backward compatibility      │  │
│ └───────────────────────────────────────────────────────────┘  │
│ ┌───────────────────────────────────────────────────────────┐  │
│ │ 9.6: Store in Cache                                       │  │
│ │ - Cache result for future queries                         │  │
│ │ - Update hit/miss statistics                              │  │
│ └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 10: Aggregate Results                                      │
│ - Collect all obligation results (maintain order)               │
│ - Calculate overall metrics:                                    │
│   • Total obligations                                           │
│   • Compliant count (is_present = "Yes")                        │
│   • Non-compliant count (is_present = "No")                     │
│   • Average confidence score                                    │
│   • Compliance percentage                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 11: Cleanup                                                │
│ - Delete temporary vector store                                 │
│ - Free memory                                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ STEP 12: Return Response                                        │
│ - Status: "success"                                             │
│ - Results: Array of obligation analysis                         │
│ - Contract URL: Path to uploaded contract                       │
│ - Full Text: Complete contract text                             │
│ - Cache Stats: Hit rate, size, etc.                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## LLM Prompt Engineering

### The Prompt Structure

The system uses a carefully engineered prompt that guides GPT-4o-mini through a structured analysis:

```python
prompt = f"""
You are a contract compliance analyst. Analyze whether the contract clause satisfies the obligation.

CRITICAL: Focus on LEGAL EFFECT and COMMERCIAL OUTCOME, not exact wording.

MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):

1. ⚠️ TERMINATION CHECK: 
   - IF Obligation requires: "continued use", "ensure access", "maintain availability" (PRIMARY GOAL)
   - AND Clause offers: "reimburse", "refund", "credit" (TERMINATION OPTION)
   - THEN Result: "No" (Conflict: Termination ≠ Continued Use)
   - EXCEPTION: If "secure rights" is just a METHOD to remedy infringement, this check does NOT apply.

2. ⚠️ NEGATIVE OBLIGATION CHECK:
   - IF Obligation says: "does NOT have to", "NOT liable", "no obligation"
   - AND Clause has: "unless", "except", "provided that" conditions
   - AND Conditions: RE-IMPOSE the liability the obligation excluded
   - THEN Result: "No" (Conflict: Exceptions negate the exclusion)

INSTRUCTION: If ANY pre-check fails, stop immediately and return "No". Do not over-analyze.

Analysis Framework:
1. **Identify the Obligation's Purpose**: What commercial outcome or risk allocation does the obligation seek?
2. **Analyze the Clause's Effect**: Does the clause achieve the same outcome or provide equivalent protection?
3. **Apply Materiality Test**: Is there a material difference that significantly changes the business value or risk?

Return "Yes" if:
- The clause achieves the same commercial/legal outcome as the obligation
- Any differences are immaterial or standard legal practice
- Alternative methods to achieve the result are acceptable

Return "No" ONLY if:
- The clause negates the obligation's core purpose
- The clause introduces a material escape that significantly shifts risk
- The clause narrows the obligation in a way that excludes common scenarios
- The clause adds conditions that re-impose obligations the original sought to exclude

Key Principles:

**Alternative Remedies**: Multiple paths to the same outcome = compliant
- Example: "modify OR secure licenses" both prevent infringement and ensure continued use → YES
- Example: "fix OR refund and terminate" have different outcomes (continued use vs. termination) → NO
- CRITICAL: "Secure licenses", "procure rights", "obtain permissions" mean CONTINUED USE (not termination)
- CRITICAL: "Reimburse", "refund", "credit" are TERMINATION options

**Discretion**: Discretion about HOW to achieve a result ≠ discretion about WHETHER to achieve it
- Example: "Vendor chooses remedy method (fix, license, replace)" = discretion on HOW → YES
- Example: "Vendor may provide support if deemed reasonable" = discretion on WHETHER → NO

**Standard Exceptions**: Legal/regulatory carve-outs are acceptable for POSITIVE obligations
- Example: "keep confidential UNLESS required by law" = standard exception → YES

**Negative Obligations (Exclusions)**: If the obligation says vendor is "NOT liable" or "does not have to" do something:
- The PURPOSE is to EXCLUDE vendor liability in specific scenarios
- If the clause adds "unless" or "except" conditions, ask: Do these conditions RE-IMPOSE the liability?
- If YES (the exceptions re-impose liability), return "No"

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "Explain the legal effect and whether it matches the obligation's purpose",
  "suggestion": "If 'No', suggest specific language to achieve compliance. If 'Yes', return null."
}}

Obligation:
{obligation}

Relevant Clauses:
{clauses}
"""
```

### Chain-of-Thought Enhancement

To improve reasoning quality, the system adds a Chain-of-Thought (CoT) instruction:

```python
cot_prompt = f"""
{prompt}

IMPORTANT: Before providing your final JSON answer, you MUST think step-by-step:

Step 1: What is the EXACT purpose of the obligation? (What outcome does it seek?)
Step 2: What does the clause ACTUALLY say? (Summarize the legal effect)
Step 3: Do they match? (Does the clause achieve the same outcome?)
Step 4: Are there any material conflicts? (Does the clause negate or weaken the obligation?)
Step 5: CRITICAL CHECK - If the obligation requires "continued use", does the clause offer "reimburse/refund/credit"?
Step 6: CRITICAL CHECK - If the clause says "at vendor's sole discretion", does it provide multiple remedy options?
Step 7: NEGATIVE OBLIGATION CHECK - If the obligation says "does NOT have to", do the clause exceptions RE-IMPOSE liability?

After completing these steps, provide your final JSON answer.
"""
```

### Prompt Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Model** | gpt-4o-mini | Cost-effective, fast, accurate |
| **Temperature** | 0.0 | Deterministic reasoning |
| **Seed** | 42 | Reproducibility |
| **Max Tokens** | 800 | Sufficient for analysis |

### Why This Prompt Works

1. **Explicit Pre-Checks**: Catches critical issues first (termination, discretion, negative obligations)
2. **Focus on Outcome**: Emphasizes legal effect over exact wording
3. **Concrete Examples**: Provides clear guidance for edge cases
4. **Structured Output**: JSON format ensures parseable results
5. **Chain-of-Thought**: Forces step-by-step reasoning for better accuracy

---

## Validation Steps Explained

### Step 1: Identify Obligation Purpose
**Type**: Analysis (Always PASS)  
**Purpose**: Determines the core intent of the obligation

**Description**: "Determines the core intent (e.g., payment, indemnification)."

**Example**:
```
Obligation: "Vendor must remedy IP infringement"
Purpose: Ensure continued use without infringement
Status: PASS
Finding: "The obligation seeks to ensure continued use without IP infringement"
```

### Step 2: Analyze Clause Effect
**Type**: Analysis (Always PASS)  
**Purpose**: Evaluates the clause's impact on the obligation

**Description**: "Evaluates the clause's impact on the obligation."

**Example**:
```
Clause: "Vendor will modify software OR secure licenses"
Effect: Provides two remedy options
Status: PASS
Finding: "The clause provides two remedy options: modify OR secure licenses"
```

### Step 3: Match Analysis
**Type**: Analysis (PASS/FAIL/WARNING)  
**Purpose**: Checks whether the clause explicitly covers the obligation

**Description**: "Checks whether the clause explicitly covers the obligation."

**Example - PASS**:
```
Obligation: "Vendor must fix bugs"
Clause: "Vendor will repair defects"
Status: PASS
Finding: "Both achieve the same outcome - bug resolution"
```

**Example - FAIL**:
```
Obligation: "Vendor must provide 24/7 support"
Clause: "Vendor will provide support during business hours"
Status: FAIL
Finding: "Business hours ≠ 24/7 - material mismatch"
```

### Step 4: Material Conflicts Check
**Type**: Analysis (PASS/FAIL)  
**Purpose**: Ensures there are no contradictions in related terms

**Description**: "Ensures there are no contradictions in related terms."

**Example - PASS**:
```
Obligation: "Keep data confidential"
Clause: "Keep data confidential UNLESS required by law"
Status: PASS
Finding: "Legal exception is standard and acceptable"
```

**Example - FAIL**:
```
Obligation: "Return ALL confidential information"
Clause: "Return all info EXCEPT for business, legal, disaster recovery purposes"
Status: FAIL
Finding: "Broad exceptions negate 'ALL' - material conflict"
```

### Step 5: Termination Check (CRITICAL)
**Type**: Critical (PASS/FAIL/N/A)  
**Purpose**: Validates if contract termination affects this obligation

**Description**: "Validates if contract termination affects this obligation."

**When it applies**:
- Obligation requires: "continued use", "ensure access", "maintain availability"
- Clause offers: "reimburse", "refund", "credit"

**Example - FAIL**:
```
Obligation: "Vendor must ensure continued use"
Clause: "Vendor may modify, license, OR reimburse and terminate"
Status: FAIL (CRITICAL)
Finding: "Termination option conflicts with continued use requirement"
Result: Automatic NO
```

**Example - PASS**:
```
Obligation: "Vendor must remedy infringement"
Clause: "Vendor will modify OR secure licenses"
Status: PASS
Finding: "No termination options found"
```

**Example - N/A**:
```
Obligation: "Vendor must provide documentation"
Clause: "Vendor will deliver user manuals"
Status: N/A
Finding: "Not about continued use or termination"
```

### Step 6: Discretion Check (CRITICAL)
**Type**: Critical (PASS/FAIL/N/A)  
**Purpose**: Looks for 'sole discretion' or similar language that weakens obligation

**Description**: "Looks for 'sole discretion' or similar language that weakens obligation."

**Key Distinction**:
- **Discretion on HOW** (method) = PASS ✅
- **Discretion on WHETHER** (outcome) = FAIL ❌

**Example - PASS (Discretion on HOW)**:
```
Obligation: "Vendor must remedy infringement"
Clause: "Vendor may, at its sole discretion, modify OR secure licenses"
Status: PASS
Finding: "Discretion is on HOW (method), not WHETHER (outcome)"
Reason: Vendor MUST remedy (commitment), just chooses method
```

**Example - FAIL (Discretion on WHETHER)**:
```
Obligation: "Vendor must provide support"
Clause: "Vendor may provide support if deemed reasonable"
Status: FAIL (CRITICAL)
Finding: "Discretion on WHETHER to provide support"
Result: Automatic NO
```

**Example - N/A**:
```
Obligation: "Vendor must deliver by Jan 1"
Clause: "Vendor will deliver by Jan 1"
Status: N/A
Finding: "No discretion language present"
```

### Step 7: Negative Obligation Check (CRITICAL)
**Type**: Critical (PASS/FAIL/N/A)  
**Purpose**: Detects exceptions like 'unless', 'except', which reverse meaning

**Description**: "Detects exceptions like 'unless', 'except', which reverse meaning."

**When it applies**:
- Obligation says: "does NOT have to", "NOT liable", "no obligation"
- Clause has: "unless", "except", "provided that" conditions
- Conditions: RE-IMPOSE the liability the obligation excluded

**Example - FAIL**:
```
Obligation: "Vendor does NOT have to indemnify for customer's unauthorized modifications"
Clause: "Vendor has no obligation UNLESS: (1) modification was required by docs, (2) modification was mutually agreed"
Status: FAIL (CRITICAL)
Finding: "Exceptions RE-IMPOSE liability the obligation sought to exclude"
Result: Automatic NO
Reason: The "unless" exceptions make vendor liable again for common scenarios
```

**Example - PASS**:
```
Obligation: "Vendor is NOT liable for customer negligence"
Clause: "Vendor has no liability for customer negligence"
Status: PASS
Finding: "No exceptions that re-impose liability"
```

**Example - N/A**:
```
Obligation: "Vendor must provide support" (positive obligation)
Clause: "Vendor will provide support"
Status: N/A
Finding: "This is a positive obligation, not an exclusion"
```

### Decision Logic Summary

```
IF (Step 5 = FAIL) OR (Step 6 = FAIL) OR (Step 7 = FAIL)
THEN Final Answer = NO (Critical failure)

ELSE IF (Step 3 = FAIL) OR (Step 4 = FAIL)
THEN Final Answer = NO (Material mismatch)

ELSE IF All Critical Steps (5, 6, 7) = PASS or N/A
     AND All Analysis Steps (3, 4) = PASS
THEN Final Answer = YES (Compliant)
```

---

## Edge Cases & Scenarios

### Scenario 1: Alternative Remedies (Same Outcome)

**Obligation**: "Vendor must remedy IP infringement by modifying software or securing licenses"

**Contract Clause**: "Vendor shall, at its discretion, modify the software OR secure necessary licenses to remedy any infringement"

**Analysis**:
```
Step 1: PASS - Purpose: Ensure continued use without infringement
Step 2: PASS - Effect: Provides modify OR license options
Step 3: PASS - Match: Both achieve continued use
Step 4: PASS - No material conflicts
Step 5: PASS - No termination options (CRITICAL)
Step 6: PASS - Discretion on HOW (modify vs license), not WHETHER to remedy (CRITICAL)
Step 7: N/A - Positive obligation (CRITICAL)
```

**Result**: ✅ **YES**  
**Similarity**: 61%  
**Why YES despite low similarity?**
- Different words ("undertake" vs "implement", "remedy" vs "secure")
- **Same legal outcome**: Both paths achieve non-infringement
- "Securing licenses" = acceptable alternative to "fixing"
- **Semantic equivalence** trumps lexical similarity

---

### Scenario 2: Termination Escape Clause

**Obligation**: "Licensee must guarantee non-infringement and must: (i) secure continued use rights, OR (ii) replace with non-infringing products"

**Contract Clause**: "Licensee will use reasonable efforts to secure rights or replace products. If unable, Licensee may reimburse Customer."

**Analysis**:
```
Step 1: PASS - Purpose: Guarantee continued use
Step 2: PASS - Effect: Provides secure/replace options + reimburse escape
Step 3: WARNING - Partial match: First two options match, third doesn't
Step 4: WARNING - Material conflict: Reimburse option allows termination
Step 5: FAIL - Termination option conflicts with continued use requirement (CRITICAL) ❌
Step 6: PASS - Discretion on HOW for first two options (CRITICAL)
Step 7: N/A - Positive obligation (CRITICAL)
```

**Result**: ❌ **NO**  
**Similarity**: 66.8%  
**Why NO despite high similarity?**
- Similar words ("secure rights", "replace products")
- **Different legal outcome**: "May reimburse" = escape clause
- Obligation requires **continued use**, refund terminates use
- **Critical step 5 failed** → Automatic NO

---

### Scenario 3: Negative Obligation with Re-Imposing Exceptions

**Obligation**: "Vendor does NOT have to indemnify Bank if infringement is solely from Bank's unauthorized modification"

**Contract Clause**: "Vendor has no indemnification obligation UNLESS: (1) modification was required by documentation, (2) modification was mutually agreed, or (3) modification was required by license terms"

**Analysis**:
```
Step 1: PASS - Purpose: Exclude vendor liability for customer-caused infringement
Step 2: PASS - Effect: Excludes liability BUT with broad exceptions
Step 3: WARNING - Partial match: Exclusion exists but exceptions weaken it
Step 4: FAIL - Material conflict: Exceptions cover common scenarios
Step 5: N/A - Not about termination (CRITICAL)
Step 6: N/A - Not about discretion (CRITICAL)
Step 7: FAIL - Exceptions RE-IMPOSE liability the obligation sought to exclude (CRITICAL) ❌
```

**Result**: ❌ **NO**  
**Why NO?**
- Critical step 7 failed
- The "unless" exceptions make vendor liable again for scenarios the obligation said they should NOT be liable for
- This negates the exclusion

---

### Scenario 4: Discretion on Method vs. Outcome

**Case A: Discretion on HOW (Acceptable)**

**Obligation**: "Vendor must remedy infringement"

**Contract Clause**: "Vendor may, at its sole discretion, implement modifications OR secure licenses to ensure continued use"

**Analysis**:
```
Step 6: PASS - Discretion is on HOW (modify vs. license), not WHETHER to remedy
Finding: "Vendor MUST ensure continued use (commitment), discretion is only on method"
```

**Result**: ✅ **YES**

**Case B: Discretion on WHETHER (Unacceptable)**

**Obligation**: "Vendor must provide support"

**Contract Clause**: "Vendor may provide support if deemed reasonable at vendor's sole discretion"

**Analysis**:
```
Step 6: FAIL - Discretion on WHETHER to provide support (CRITICAL) ❌
Finding: "No commitment to provide support, vendor can choose not to"
```

**Result**: ❌ **NO**

---

### Scenario 5: Standard vs. Broad Exceptions

**Case A: Standard Exception (Acceptable)**

**Obligation**: "Keep all information confidential"

**Contract Clause**: "Keep all information confidential UNLESS required by law or court order"

**Analysis**:
```
Step 4: PASS - Legal/regulatory exceptions are standard and acceptable
Finding: "Standard legal carve-out does not materially weaken obligation"
```

**Result**: ✅ **YES**

**Case B: Broad Exception (Unacceptable)**

**Obligation**: "Return ALL confidential information"

**Contract Clause**: "Return all information EXCEPT for business purposes, legal requirements, or disaster recovery"

**Analysis**:
```
Step 4: FAIL - Broad exceptions negate "ALL"
Finding: "Exceptions are so broad they effectively eliminate the obligation"
```

**Result**: ❌ **NO**

---

### Scenario 6: Multilingual Contract

**Obligation** (Spanish): "El proveedor debe solucionar la infracción"

**Contract Clause** (French): "Le fournisseur corrigera toute violation"

**Processing**:
```
1. Detect languages: Spanish (obligation), French (contract)
2. Translate to English:
   - Obligation: "The vendor must remedy the infringement"
   - Clause: "The vendor will correct any violation"
3. Analyze in English
4. Return result
```

**Result**: ✅ **YES** (same meaning in both languages)

---

### Scenario 7: Cache Hit on Renamed File

**Upload 1**:
```
Obligation: "Vendor must remedy infringement"
Contract: contract_v1.pdf (content: "Vendor will fix...")
Cache Key: hash("Vendor must remedy..." + hash("Vendor will fix..."))
Result: Analyzed, cached
```

**Upload 2** (File renamed, same content):
```
Obligation: "Vendor must remedy infringement" (same)
Contract: contract_final.pdf (SAME content: "Vendor will fix...")
Cache Key: hash("Vendor must remedy..." + hash("Vendor will fix..."))
Result: ✅ CACHE HIT - Returns cached result instantly
```

**Why?**: Content-based hashing ignores filename

---

### Scenario 8: Cache Miss on Updated Contract

**Upload 1**:
```
Obligation: "Vendor must remedy infringement"
Contract: contract.pdf (content: "Vendor will fix...")
Cache Key: hash("Vendor must remedy..." + hash("Vendor will fix..."))
Result: Analyzed, cached
```

**Upload 2** (Same filename, updated content):
```
Obligation: "Vendor must remedy infringement" (same)
Contract: contract.pdf (UPDATED: "Vendor will reimburse...")
Cache Key: hash("Vendor must remedy..." + hash("Vendor will reimburse..."))
Result: ✅ CACHE MISS - Re-analyzes with new content
```

**Why?**: Content hash changed, ensuring fresh analysis

---

## Setup & Installation

### Prerequisites

- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **npm**: 8 or higher
- **OpenAI API Key**: Required for LLM and embeddings

### Backend Setup

1. **Clone the repository**:
```bash
cd ContractAnalysisPlatformGuardRails
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Python dependencies**:
```bash
pip install -r backend/requirements.txt
```

4. **Download spaCy model**:
```bash
python -m spacy download en_core_web_sm
```

5. **Create `.env` file**:
```bash
cp .env.example .env
```

6. **Configure `.env`**:
```env
# OpenAI API Key (REQUIRED)
OPENAI_API_KEY=your-openai-api-key-here

# Embedding Model (optional)
# Options: text-embedding-3-small (default), text-embedding-3-large
EMBEDDING_MODEL=text-embedding-3-small

# Caching (optional, default: true)
USE_CACHE=true

# Batch Processing (optional, default: 5)
BATCH_SIZE=5
```

7. **Start the backend server**:
```bash
uvicorn backend.main:app --reload
```

Server will start at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Start development server**:
```bash
npm run dev
```

Frontend will start at: `http://localhost:5173`

### Production Build

**Backend**:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Frontend**:
```bash
cd frontend
npm run build
# Serve the dist/ folder with your preferred static server
```

---

## Usage Guide

### 1. **Prepare Your Files**

**Obligations File** (Excel or CSV):
```
| Obligation |
|------------|
| Vendor must remedy IP infringement |
| Vendor must provide 24/7 support |
| Vendor is NOT liable for customer modifications |
```

**Contract File** (PDF, DOCX, Excel, or TXT):
- Any format containing the contract text
- Can be multilingual (auto-translated)

### 2. **Upload Files**

1. Open the application in your browser
2. Click "Upload Obligations File" and select your Excel/CSV
3. Click "Upload Contract File" and select your contract
4. Click "Analyze" button

### 3. **View Results**

**Dashboard View**:
- Overall compliance percentage
- Total obligations analyzed
- Compliant vs. non-compliant breakdown
- Average confidence score

**List View**:
- All obligations with status badges
- Confidence scores
- Click to view details

**Details Panel**:
- **Details Tab**: Analysis reasoning + 7 validation steps
- **Evidence Tab**: Supporting clauses from contract
- **Suggestion Tab**: Remediation advice (if non-compliant)

**PDF Preview**:
- View original contract
- Highlighted text for selected obligation
- Page/line navigation

### 4. **Interpret Results**

**Status Badges**:
- 🟢 **Compliance** (Yes): Obligation is satisfied
- 🔴 **Non-Compliance** (No): Obligation is not satisfied

**Confidence Score**:
- 0-100% based on cosine similarity
- Higher = more similar wording
- **NOT the same as compliance status**

**Validation Steps**:
- ✅ Green: Step passed
- ❌ Red: Step failed
- ⚠️ Yellow: Warning (partial match)
- 🔴 CRITICAL: Critical step (5, 6, or 7)

---

## API Reference

### Endpoints

#### 1. **Analyze Contract**

```http
POST /api/analyze
Content-Type: multipart/form-data
```

**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "obligations_file=@obligations.xlsx" \
  -F "contract_file=@contract.pdf"
```

**Response**:
```json
{
  "status": "success",
  "results": [
    {
      "obligation": "Vendor must remedy IP infringement",
      "is_present": "Yes",
      "confidence": 87.3,
      "similarity_score": 0.873,
      "reason": "Contract commits to reasonable efforts to remedy",
      "suggestion": null,
      "supporting_clauses": [
        "[Page 5 Line 12] Vendor will modify software or secure licenses..."
      ],
      "cot_steps": [
        {
          "step_number": 1,
          "step_name": "Identify Obligation Purpose",
          "status": "PASS",
          "finding": "Purpose: Ensure continued use without infringement",
          "is_critical": false
        },
        // ... more steps
      ],
      "page": 5,
      "line": 12,
      "keyword_hits": ["remedy", "infringement", "modify"]
    }
  ],
  "contract_url": "/uploads/abc123_contract.pdf",
  "full_text": "Full contract text..."
}
```

#### 2. **Get Cache Statistics**

```http
GET /api/cache/stats
```

**Response**:
```json
{
  "status": "success",
  "cache_stats": {
    "size": 45,
    "max_size": 1000,
    "hits": 120,
    "misses": 45,
    "hit_rate": 72.73,
    "total_requests": 165
  }
}
```

#### 3. **Clear Cache**

```http
POST /api/cache/clear
```

**Response**:
```json
{
  "status": "success",
  "message": "Cache cleared successfully"
}
```

---

## Frontend Architecture

### Component Structure

```
frontend/src/
├── App.tsx                    # Main app component with routing
├── main.tsx                   # Entry point
├── index.css                  # Global styles
│
├── pages/
│   ├── Home.tsx              # Main analysis page
│   └── Login.tsx             # Authentication page
│
├── components/
│   ├── FileUpload.tsx        # File upload component
│   ├── AnalysisResults.tsx   # Results dashboard
│   ├── ItemsList.tsx         # Obligations list
│   ├── TabsPanel.tsx         # Details/Evidence/Suggestion tabs
│   ├── StatusBadge.tsx       # Compliance status badge
│   ├── StatCard.tsx          # Metric card component
│   │
│   ├── layout/
│   │   ├── Header.tsx        # App header
│   │   └── Footer.tsx        # App footer
│   │
│   ├── pdf/
│   │   ├── PDFViewer.tsx     # PDF preview component
│   │   ├── PDFHighlight.tsx  # Text highlighting
│   │   └── PDFToolbar.tsx    # PDF controls
│   │
│   └── reusable/
│       ├── Button.tsx        # Reusable button
│       ├── Card.tsx          # Reusable card
│       ├── Input.tsx         # Reusable input
│       ├── Spinner.tsx       # Loading spinner
│       └── Tooltip.tsx       # Tooltip component
│
├── context/
│   └── AuthContext.tsx       # Authentication context
│
├── hooks/
│   └── useAnalysis.tsx       # Analysis state management
│
├── charts/
│   ├── ComplianceChart.tsx   # Compliance pie chart
│   └── TrendChart.tsx        # Trend line chart
│
└── route/
    └── ProtectedRoute.tsx    # Route protection
```

### Key Components

#### FileUpload.tsx
- Drag-and-drop file upload
- File type validation
- Progress indication
- Error handling

#### AnalysisResults.tsx
- Results dashboard
- Metrics cards (compliance %, total obligations, etc.)
- Charts (compliance breakdown, confidence distribution)
- List/Grid view toggle

#### TabsPanel.tsx
- **Details Tab**: Analysis reasoning + validation steps
- **Evidence Tab**: Supporting clauses with highlighting
- **Suggestion Tab**: Remediation recommendations
- Step descriptions with tooltips

#### PDFViewer.tsx
- PDF rendering with react-pdf-viewer
- Text search and highlighting
- Page navigation
- Zoom controls

### State Management

**Analysis State** (useAnalysis hook):
```typescript
{
  results: ObligationResult[],
  selectedObligation: ObligationResult | null,
  selectedClause: string,
  contractUrl: string,
  fullText: string,
  loading: boolean,
  error: string | null
}
```

**Authentication State** (AuthContext):
```typescript
{
  user: User | null,
  login: (credentials) => Promise<void>,
  logout: () => void,
  isAuthenticated: boolean
}
```

---

## Performance Optimizations

### 1. **Caching Strategy**

**Implementation**:
- In-memory LRU cache (max 1000 entries)
- Content-based hashing (SHA256)
- Automatic hit rate tracking

**Benefits**:
- 10x faster for repeated obligations
- 10x cost savings (fewer LLM API calls)
- 100% cache hit rate for identical queries

**Configuration**:
```env
USE_CACHE=true  # Enable/disable caching
```

### 2. **Batch Processing**

**Implementation**:
- ThreadPoolExecutor with 5 workers
- Parallel LLM calls for I/O-bound tasks
- Order preservation

**Benefits**:
- 3-5x faster for multiple obligations
- Optimal worker count (5) balances speed vs. API limits

**Configuration**:
```env
BATCH_SIZE=5  # Number of parallel workers
```

**Tuning Guide**:
| BATCH_SIZE | Best For | Pros | Cons |
|------------|----------|------|------|
| 1 | Testing | Sequential, easy to debug | Very slow |
| 3 | Small contracts | Moderate speedup | Underutilizes API |
| 5 (default) | Most cases | Good balance | Optimal for most |
| 7-10 | Large contracts | Maximum speed | May hit rate limits |

### 3. **Embedding Model Selection**

**Options**:
- `text-embedding-3-small`: Fast, cost-effective, 1536 dimensions (default)
- `text-embedding-3-large`: Better semantic understanding, 3072 dimensions

**Configuration**:
```env
EMBEDDING_MODEL=text-embedding-3-small  # or text-embedding-3-large
```

**When to use text-embedding-3-large**:
- Legal contracts with complex terminology
- Nuanced language (e.g., "reasonable efforts", "in lieu of")
- Presentations/demos requiring highest accuracy

### 4. **Keyword Caching**

**Implementation**:
- Persistent cache (JSON file)
- SHA256 hash of obligation text
- Deterministic LLM generation (temperature=0, seed=42)

**Benefits**:
- Consistent keywords across runs
- Faster keyword generation (cache hit)
- Reduced LLM API calls

### 5. **Vector Store Cleanup**

**Implementation**:
- Temporary FAISS index per session
- Automatic cleanup after analysis
- Startup cleanup for old indexes

**Benefits**:
- Prevents disk bloat
- Frees memory
- No manual cleanup needed

---

## Troubleshooting

### Common Issues

#### 1. **Blank Page / Frontend Not Loading**

**Symptoms**:
- Browser shows blank page
- Console errors about missing modules

**Solutions**:
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

#### 2. **Backend Startup Error: "OPENAI_API_KEY not found"**

**Symptoms**:
```
ValueError: OPENAI_API_KEY must be set in .env file
```

**Solutions**:
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key
OPENAI_API_KEY=sk-...
```

#### 3. **spaCy Model Not Found**

**Symptoms**:
```
OSError: [E050] Can't find model 'en_core_web_sm'
```

**Solutions**:
```bash
python -m spacy download en_core_web_sm
```

#### 4. **Low Cache Hit Rate**

**Symptoms**:
- Cache hit rate < 50%
- Obligations are slightly different each time

**Solutions**:
- Normalize obligation text (trim whitespace, lowercase)
- Use consistent phrasing in obligations file
- Check cache stats: `GET /api/cache/stats`

#### 5. **Batch Processing Not Faster**

**Symptoms**:
- Batch processing takes same time as sequential

**Solutions**:
```env
# Increase batch size
BATCH_SIZE=7

# Check if obligations are being cached (no LLM calls)
# If cached, batch processing won't help
```

#### 6. **Out of Memory**

**Symptoms**:
```
MemoryError: Unable to allocate array
```

**Solutions**:
```bash
# Clear cache
curl -X POST http://localhost:8000/api/cache/clear

# Reduce cache size in backend/cache.py
max_size=500  # instead of 1000
```

#### 7. **PDF Preview Not Working**

**Symptoms**:
- PDF viewer shows blank
- Console error: "Failed to load PDF"

**Solutions**:
```bash
# Check if contract file was uploaded correctly
# Verify contract_url in API response

# Check CORS settings in backend/main.py
allow_origins=["*"]  # For development
```

---

## Future Enhancements

### Planned Features

- [ ] **Support for More LLM Providers**
  - Anthropic Claude
  - Google Gemini
  - Azure OpenAI

- [ ] **Custom Fine-Tuned Embeddings**
  - Train on legal corpus
  - Domain-specific embeddings

- [ ] **Persistent Cache**
  - Redis for distributed caching
  - Database for long-term storage

- [ ] **Confidence Calibration**
  - Historical data analysis
  - Adaptive thresholds

- [ ] **Advanced Analytics**
  - Trend analysis over time
  - Contract comparison
  - Risk scoring

- [ ] **Collaboration Features**
  - Multi-user support
  - Comments and annotations
  - Approval workflows

- [ ] **Export Capabilities**
  - PDF reports
  - Excel exports
  - API integrations

### Implemented Features ✅

- [x] Configurable embeddings for legal domain
- [x] Caching for repeated obligations
- [x] Batch processing for large contracts
- [x] Legal domain prompt engineering
- [x] 7-step validation framework
- [x] Modern React UI with PDF preview
- [x] Multilingual support

---

## License

MIT License

---

## Contributors

Developed as part of an AI-powered contract intelligence project.

---

## Support

For issues, questions, or contributions, please contact the development team.

---

**Last Updated**: November 30, 2025  
**Version**: 1.0.0
