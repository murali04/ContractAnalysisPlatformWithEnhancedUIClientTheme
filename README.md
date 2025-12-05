# 🤖 AI-Powered Contract Analysis Platform

> **Intelligent contract compliance validation using advanced NLP, semantic search, and LLM reasoning**

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)](https://openai.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Contract Analysis Platform** is an enterprise-grade AI solution that automatically validates whether contract clauses satisfy specified obligations. It combines cutting-edge technologies including:

- **Semantic Search (RAG)** - Vector-based similarity matching
- **LLM Reasoning** - GPT-4o-mini for intelligent analysis
- **Multi-language Support** - Automatic translation
- **7-Step Validation** - Comprehensive compliance framework

### Use Cases

✅ **Legal Teams** - Validate contract compliance at scale  
✅ **Procurement** - Ensure vendor agreements meet requirements  
✅ **Risk Management** - Identify contractual gaps and risks  
✅ **Compliance Officers** - Audit contracts against policies  

---

## ✨ Key Features

### 🔍 Intelligent Analysis
- **Semantic Understanding** - Goes beyond keyword matching to understand legal intent
- **Context-Aware** - Analyzes commercial outcomes, not just exact wording
- **Multi-format Support** - PDF, DOCX, Excel, CSV, TXT

### 🌐 Multi-language
- **Auto-detection** - Identifies document language automatically
- **Translation** - Converts to English for analysis
- **Supported Languages** - English, Spanish, French, German, Italian, Portuguese, Hindi

### 🎨 Rich UI
- **Interactive Dashboard** - Real-time compliance metrics
- **PDF Highlighting** - Visual clause identification
- **Detailed Reports** - Step-by-step validation breakdown
- **Export Options** - CSV download for further analysis

### ⚡ Performance
- **Caching** - 60-80% faster for repeated obligations
- **Batch Processing** - Parallel analysis for speed
- **Optimized Embeddings** - Fast vector search

---

## 🎬 Demo

### Upload Files
![Upload Interface](docs/upload-demo.png)

### Analysis Results
![Analysis Dashboard](docs/results-demo.png)

### Validation Steps
![Validation Details](docs/validation-demo.png)

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+
- **Node.js** 16+
- **OpenAI API Key**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/contract-analysis-platform.git
cd contract-analysis-platform
```

2. **Set up Backend**
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

3. **Set up Frontend**
```bash
cd frontend
npm install
```

4. **Run the Application**

**Terminal 1 - Backend:**
```bash
uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

5. **Access the Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔧 How It Works

### 1️⃣ Input Processing

**Obligations File** (Excel/CSV)
```
| Obligation                                    |
|-----------------------------------------------|
| Vendor must provide 24/7 technical support   |
| All data must be encrypted at rest           |
| Vendor shall indemnify customer              |
```

**Contract File** (PDF/DOCX/TXT)
```
Any standard contract document in supported format
```

### 2️⃣ Analysis Pipeline

```mermaid
graph LR
    A[Upload Files] --> B[Language Detection]
    B --> C[Translation]
    C --> D[Text Extraction]
    D --> E[Chunking]
    E --> F[Vector Embeddings]
    F --> G[Semantic Search]
    G --> H[LLM Analysis]
    H --> I[Validation Steps]
    I --> J[Results]
```

### 3️⃣ Validation Framework

The platform performs **7 critical validation steps**:

1. **Identify Obligation Purpose** - Extract core intent
2. **Analyze Clause Effect** - Determine actual legal effect
3. **Match Analysis** - Compare purpose vs. effect
4. **Material Conflicts Check** - Identify contradictions
5. **Termination Check** ⚠️ - Detect unwanted termination options
6. **Discretion Check** ⚠️ - Distinguish HOW vs. WHETHER discretion
7. **Negative Obligation Check** ⚠️ - Verify exclusions aren't negated

### 4️⃣ Output

```json
{
  "obligation": "Vendor must provide 24/7 support",
  "is_present": "No",
  "reason": "Clause only commits to business hours support",
  "confidence": 87.5,
  "page": 5,
  "line": 23,
  "suggestion": "Add: 'Support available 24/7/365'",
  "cot_steps": [...]
}
```

---

## 🛠 Tech Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI Framework |
| TypeScript | Type Safety |
| Vite | Build Tool |
| Tailwind CSS | Styling |
| Recharts | Data Visualization |
| React PDF Viewer | Document Display |
| Axios | HTTP Client |

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | Web Framework |
| OpenAI GPT-4o-mini | LLM Analysis |
| text-embedding-3-small | Vector Embeddings |
| FAISS | Vector Search |
| spaCy | NLP Processing |
| PyMuPDF | PDF Parsing |
| pandas | Data Processing |
| scikit-learn | Similarity Calculation |

---

## 📁 Project Structure

```
contract-analysis-platform/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── core.py                 # Core analysis engine
│   ├── core_enhanced.py        # Enhanced features (caching, batching)
│   ├── cache.py                # LRU cache implementation
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx       # File upload interface
│   │   │   ├── AnalysisResults.tsx  # Results dashboard
│   │   │   ├── ItemsList.tsx        # Obligations list
│   │   │   ├── PdfContainer.tsx     # PDF viewer
│   │   │   └── TabsPanel.tsx        # Detailed analysis tabs
│   │   ├── charts/
│   │   │   ├── RadialHealthChart.tsx
│   │   │   └── StatusBarChart.tsx
│   │   └── context/
│   │       └── AuthContext.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── uploads/                    # Uploaded contract files
├── user_memory/                # Vector stores & cache
│   └── keyword_cache/          # Persistent keyword cache
│
├── .env                        # Environment variables
├── .env.example                # Environment template
├── README.md                   # This file
└── TECHNICAL_DOCUMENTATION.md  # Detailed technical docs
```

---

## 📡 API Documentation

### Main Endpoints

#### `POST /api/analyze/enhanced`
Analyze contract against obligations with enhanced features.

**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze/enhanced" \
  -F "obligations_file=@obligations.xlsx" \
  -F "contract_file=@contract.pdf" \
  -F "use_batch=true"
```

**Response:**
```json
{
  "status": "success",
  "results": [...],
  "contract_url": "/uploads/abc123_contract.pdf",
  "full_text": "...",
  "cache_stats": {
    "hits": 5,
    "misses": 3,
    "hit_rate": 0.625
  }
}
```

#### `GET /api/cache/stats`
Get cache performance statistics.

#### `POST /api/cache/clear`
Clear all cached results.

**Full API Documentation:** http://localhost:8000/docs (when running)

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional (with defaults)
EMBEDDING_MODEL=text-embedding-3-small  # or text-embedding-3-large
USE_CACHE=true
BATCH_SIZE=5
LOG_LEVEL=INFO
```

### Model Selection

**text-embedding-3-small** (Default)
- Dimensions: 1536
- Speed: Fast
- Cost: Lower
- Use for: Production, high-volume

**text-embedding-3-large**
- Dimensions: 3072
- Speed: Slower
- Cost: Higher
- Use for: Maximum accuracy

### Performance Tuning

```python
# In core.py
CHUNK_SIZE = 1500        # Characters per chunk
CHUNK_OVERLAP = 300      # Overlap for context
TOP_K = 10               # Documents to retrieve
MAX_RETRIES = 3          # LLM retry attempts
```

---

## 🐛 Troubleshooting

### Common Issues

**1. "OPENAI_API_KEY not found"**
```bash
# Ensure .env file exists and contains:
OPENAI_API_KEY=sk-...
```

**2. "spaCy model not found"**
```bash
python -m spacy download en_core_web_sm
```

**3. "Port already in use"**
```bash
# Backend (change port)
uvicorn backend.main:app --reload --port 8001

# Frontend (change port in vite.config.ts)
```

**4. "CORS errors"**
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`

**5. "Out of memory"**
```bash
# Reduce batch size in .env
BATCH_SIZE=3

# Or disable batch processing
use_batch=false
```

### Debug Mode

Enable detailed logging:
```bash
# In .env
LOG_LEVEL=DEBUG
```

Check logs:
```bash
# Backend logs
tail -f backend.log

# Frontend console
Open browser DevTools > Console
```

---

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| File Upload | < 1s |
| PDF Extraction (50 pages) | 2-3s |
| Vector Store Creation | 3-5s |
| Keyword Generation (10 obligations) | 5-8s (first), < 1s (cached) |
| Semantic Search (per obligation) | 0.5-1s |
| LLM Analysis (per obligation) | 2-4s |
| **Total (10 obligations)** | **30-45s (sequential)** |
| **Total (10 obligations, batched)** | **15-20s (parallel)** |

### Optimization Results
- **Caching:** 60-80% faster for repeated obligations
- **Batch Processing:** 40-50% faster for multiple obligations
- **Persistent Cache:** 90% faster on subsequent runs

---

## 🧪 Testing

### Run Tests
```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend
npm test
```

### Example Test Cases

**Test 1: Exact Match**
- Obligation: "Vendor must encrypt data"
- Clause: "All data shall be encrypted using AES-256"
- Expected: ✅ PASS

**Test 2: Semantic Match**
- Obligation: "Vendor must fix bugs"
- Clause: "Vendor will repair all defects"
- Expected: ✅ PASS

**Test 3: Termination Conflict**
- Obligation: "Vendor must ensure continued use"
- Clause: "Vendor may refund and terminate"
- Expected: ❌ FAIL (Termination Check)

**Test 4: Discretion Issue**
- Obligation: "Vendor must provide support"
- Clause: "Vendor may provide support at its discretion"
- Expected: ❌ FAIL (Discretion Check)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for TypeScript
- Add tests for new features
- Update documentation

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini and embeddings
- Facebook AI for FAISS vector search
- spaCy for NLP capabilities
- React and FastAPI communities

---

## 📞 Support

- **Documentation:** [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)
- **Issues:** [GitHub Issues](https://github.com/yourusername/contract-analysis-platform/issues)
- **Email:** support@yourcompany.com

---

## 🗺️ Roadmap

- [ ] Support for more document formats (HTML, RTF)
- [ ] Custom validation rules
- [ ] Multi-contract comparison
- [ ] Integration with document management systems
- [ ] Advanced analytics dashboard
- [ ] API rate limiting and authentication
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, Azure, GCP)

---

**Made with ❤️ by the Contract Analysis Team**

*Last Updated: December 3, 2025*
