import os
import shutil
import uuid
import logging
import json
import hashlib
import fitz  # PyMuPDF
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from keybert import KeyBERT
from openai import OpenAI
from langdetect import detect
from googletrans import Translator
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from sklearn.metrics.pairwise import cosine_similarity
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
load_dotenv()
logger = logging.getLogger(__name__)

# Validate environment variables
if not os.getenv("OPENAI_API_KEY"):
    logger.error("OPENAI_API_KEY not found in environment variables!")
    raise ValueError("OPENAI_API_KEY must be set in .env file")

# Initialize globals
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = OpenAIEmbeddings(model="text-embedding-3-small")
kw_model = KeyBERT()
translator = Translator()

import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Download if not present (though usually better to do in docker/setup)
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

USER_DIR = "user_memory"
os.makedirs(USER_DIR, exist_ok=True)

# Keyword cache directory
KEYWORD_CACHE_DIR = os.path.join(USER_DIR, "keyword_cache")
os.makedirs(KEYWORD_CACHE_DIR, exist_ok=True)
KEYWORD_CACHE_FILE = os.path.join(KEYWORD_CACHE_DIR, "keywords.json")

# Load keyword cache from disk
def load_keyword_cache():
    """Load keyword cache from disk."""
    if os.path.exists(KEYWORD_CACHE_FILE):
        try:
            with open(KEYWORD_CACHE_FILE, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                logger.info(f"Loaded keyword cache with {len(cache)} entries")
                return cache
        except Exception as e:
            logger.warning(f"Failed to load keyword cache: {e}")
            return {}
    return {}

def save_keyword_cache(cache):
    """Save keyword cache to disk."""
    try:
        with open(KEYWORD_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved keyword cache with {len(cache)} entries")
    except Exception as e:
        logger.error(f"Failed to save keyword cache: {e}")

def get_cache_key(obligation):
    """Generate cache key for an obligation."""
    return hashlib.sha256(obligation.encode('utf-8')).hexdigest()

# Initialize keyword cache
_keyword_cache = load_keyword_cache()

logger.info("Core module initialized successfully")

def detect_language(text):
    try:
        lang_code = detect(text)
        flags = {
            "en": "🇬🇧", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪",
            "it": "🇮🇹", "pt": "🇵🇹", "hi": "🇮🇳", "unknown": "🌐"
        }
        return flags.get(lang_code, "🌐")
    except Exception:
        return "🌐"

def translate_to_english(text):
    try:
        lang_code = detect(text)
        if lang_code != "en" and lang_code != "unknown":
            try:
                translated = translator.translate(text, src=lang_code, dest="en")
                return translated.text
            except Exception:
                # fallback to OpenAI translate if googletrans fails
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Translate the following text to English precisely."},
                        {"role": "user", "content": text}
                    ],
                    temperature=0
                )
                return resp.choices[0].message.content.strip()
        return text
    except Exception:
        return text

def get_user_vector_path(session_id):
    run_id = str(uuid.uuid4())[:8]
    return os.path.join(USER_DIR, f"faiss_{session_id}_{run_id}")

def extract_text_from_pdf(file_bytes):
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    records = []
    for page_num, page in enumerate(pdf, start=1):
        lines = page.get_text("text").split("\n")
        for line_num, line in enumerate(lines, start=1):
            if line.strip():
                records.append({"page": page_num, "line": line_num, "text": line.strip()})
    pdf.close()
    return records

def extract_text_from_docx(file_bytes):
    from docx import Document as DocxDocument
    import io
    doc = DocxDocument(io.BytesIO(file_bytes))
    return [{"page": 1, "line": i + 1, "text": p.text.strip()} for i, p in enumerate(doc.paragraphs) if p.text.strip()]

def extract_text_from_excel(file_bytes):
    import io
    df = pd.read_excel(io.BytesIO(file_bytes)).dropna(how="all")
    df.columns = [str(c).strip() for c in df.columns]
    lines = [" | ".join(map(str, row)) for _, row in df.iterrows()]
    return [{"page": 1, "line": i + 1, "text": t} for i, t in enumerate(lines)]

def extract_text_from_txt(file_bytes):
    text = file_bytes.decode("utf-8")
    return [{"page": 1, "line": i+1, "text": l.strip()} for i, l in enumerate(text.split("\n")) if l.strip()]

def chunk_text(records):
    # CRITICAL FIX: Group text by page first to avoid fragmenting into single lines
    # Also preserve line number information for each chunk with accurate tracking
    pages = {}
    page_line_map = {}  # Track line numbers for each page
    
    for rec in records:
        p = rec.get("page", 1)
        line = rec.get("line", 1)
        
        if p not in pages:
            pages[p] = []
            page_line_map[p] = []
        
        pages[p].append(rec["text"])
        page_line_map[p].append(line)
        
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    docs = []
    
    for page_num, lines in pages.items():
        # Reconstruct page text with line tracking
        page_text = "\n".join(lines)
        line_numbers = page_line_map[page_num]
        
        # Get the starting line number for this page
        starting_line = line_numbers[0] if line_numbers else 1
        
        # Split into meaningful chunks
        chunks = splitter.split_text(page_text)
        
        # Calculate line numbers more accurately
        current_char_pos = 0
        for idx, chunk in enumerate(chunks):
            # Find which line this chunk starts at by counting newlines up to this point
            text_before_chunk = page_text[:current_char_pos]
            lines_before = text_before_chunk.count('\n')
            
            # Calculate the actual line number for this chunk
            if lines_before < len(line_numbers):
                chunk_line = line_numbers[lines_before]
            else:
                # Fallback if we're beyond tracked lines
                chunk_line = starting_line + lines_before
            
            docs.append(Document(
                page_content=chunk, 
                metadata={"page": page_num, "line": chunk_line, "chunk_id": idx}
            ))
            
            # Update position for next chunk
            current_char_pos += len(chunk)
            
    return docs

def build_vector_store(docs, path):
    if os.path.exists(path):
        shutil.rmtree(path)
    vs = FAISS.from_documents(docs, embedder)
    vs.save_local(path)
    return vs

def generate_dynamic_keywords(obligations):
    """Generate keywords for obligations with persistent caching for consistency."""
    global _keyword_cache
    keywords_dict = {}
    cache_updated = False
    
    for ob in obligations:
        cache_key = get_cache_key(ob)
        
        # Check cache first
        if cache_key in _keyword_cache:
            keywords_dict[ob] = _keyword_cache[cache_key]
            logger.info(f"Using cached keywords for: {ob[:50]}...")
            continue
        
        # Generate new keywords if not in cache
        try:
            logger.info(f"Generating keywords for: {ob[:50]}...")
            
            # Dynamic LLM-based keyword generation for generic applicability
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a legal search expert. Return a JSON object with a key 'keywords' containing 5-8 search terms for the given obligation. \n\nCRITICAL: You must predict the **exact words** a vendor would use to **limit** or **avoid** this obligation.\n- Example: If obligation is 'fix', search for 'refund', 'credit', 'obsolescence'.\n- Example: If obligation is 'indemnify', search for 'defend', 'hold harmless', 'control of defense'.\n- Example: If obligation is 'unlimited', search for 'cap', 'aggregate liability', 'fees paid'.\n\nFocus on specific nouns and verbs found in the contract text."},
                    {"role": "user", "content": ob}
                ],
                temperature=0.0,  # Changed from 0.2 to 0.0 for determinism
                seed=42,  # Added seed for reproducibility
                response_format={"type": "json_object"}
            )
            res_text = response.choices[0].message.content
            logger.debug(f"LLM keyword response for '{ob[:30]}...': {res_text}")
            
            parsed = json.loads(res_text)
            keywords = parsed.get("keywords", [])
            
            # HYBRID STRATEGY: Combine LLM's context-aware keywords with a "Universal Safety Net"
            # These terms are universally relevant for finding limitations/escapes in ANY contract.
            universal_danger_words = ["refund", "reimburse", "terminate", "cap", "limit", "sole discretion", "exclusive remedy", "unless", "except", "notwithstanding", "subject to", "provided that"]
            keywords.extend(universal_danger_words)
            
            # Deduplicate and sort for consistency
            keywords = sorted(list(set(keywords)))
            keywords_dict[ob] = keywords
            
            # Cache the result
            _keyword_cache[cache_key] = keywords
            cache_updated = True
            
        except Exception as e:
            logger.error(f"Keyword generation failed for '{ob}': {e}")
            # Fallback: simple noun chunks + danger words
            try:
                doc = nlp(ob)
                base_kws = [chunk.text.lower() for chunk in doc.noun_chunks]
                base_kws.extend(["refund", "reimburse", "terminate", "cap", "limit"])
                keywords = sorted(list(set(base_kws)))
                keywords_dict[ob] = keywords
                _keyword_cache[cache_key] = keywords
                cache_updated = True
            except:
                keywords = sorted(ob.split()[:5] + ["refund", "reimburse", "terminate"])
                keywords_dict[ob] = keywords
                _keyword_cache[cache_key] = keywords
                cache_updated = True
    
    # Save cache if updated
    if cache_updated:
        save_keyword_cache(_keyword_cache)
                
    return keywords_dict


def create_fallback_steps(final_status, reason):
    """
    Generate step-by-step visualization based on the final decision and reason.
    Since we reverted to the original prompt for accuracy, we reconstruct the steps
    here to provide the UI with the expected data structure.
    """
    reason_lower = reason.lower() if reason else ""
    
    # Default: All PASS if Yes, FAIL on match/conflict if No
    steps = [
        {"step_number": 1, "step_name": "Identify Obligation Purpose", "status": "PASS", "finding": "Obligation purpose identified.", "is_critical": False},
        {"step_number": 2, "step_name": "Analyze Clause Effect", "status": "PASS", "finding": "Clause effect analyzed.", "is_critical": False},
        {"step_number": 3, "step_name": "Match Analysis", "status": "PASS", "finding": "Clause matches obligation.", "is_critical": False},
        {"step_number": 4, "step_name": "Material Conflicts Check", "status": "PASS", "finding": "No material conflicts found.", "is_critical": False},
        {"step_number": 5, "step_name": "Termination Check", "status": "PASS", "finding": "No termination options found.", "is_critical": True},
        {"step_number": 6, "step_name": "Discretion Check", "status": "PASS", "finding": "Discretion is acceptable.", "is_critical": True},
        {"step_number": 7, "step_name": "Negative Obligation Check", "status": "N/A", "finding": "Not applicable.", "is_critical": True}
    ]
    
    if final_status == "No":
        # Heuristic: Try to identify which step failed based on keywords in the reason
        
        # Step 5: Termination Check
        if any(x in reason_lower for x in ["refund", "reimburse", "credit", "termination option"]):
            steps[4]["status"] = "FAIL"
            steps[4]["finding"] = reason
            steps[2]["status"] = "WARNING" # Match analysis likely partial
        
        # Step 6: Discretion Check
        elif any(x in reason_lower for x in ["discretion", "sole discretion", "may provide"]):
            steps[5]["status"] = "FAIL"
            steps[5]["finding"] = reason
            steps[2]["status"] = "WARNING"
            
        # Step 7: Negative Obligation Check
        elif any(x in reason_lower for x in ["exception", "unless", "re-impose", "negate exclusion"]):
            steps[6]["status"] = "FAIL"
            steps[6]["finding"] = reason
            steps[6]["status"] = "FAIL" # Set status to FAIL (was N/A)
            
        # Default: Match Analysis or Material Conflict
        else:
            steps[2]["status"] = "FAIL"
            steps[2]["finding"] = reason
            steps[3]["status"] = "FAIL"
            steps[3]["finding"] = "Material differences found."
            
    return steps

def query_rag(vs, obligation, auto_keywords, top_k=10):
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": top_k})
    docs = retriever.get_relevant_documents(obligation)
    
    if not docs:
        return {
            "obligation": obligation, "is_present": "No", "reason": "No relevant clauses retrieved.",
            "similarity_score": 0.0, "keyword_hits": [], "confidence": 0.0,
            "page": None, "line": None, "supporting_clauses": [],
            "suggestion": "Unable to find relevant clauses in the contract.",
            "cot_steps": create_fallback_steps("No", "No relevant clauses retrieved.")
        }
    
    ob_emb = embedder.embed_query(obligation)
    doc_embs = [embedder.embed_query(d.page_content) for d in docs]
    sims = cosine_similarity([ob_emb], doc_embs)[0]
    best_idx = int(np.argmax(sims))
    best_doc = docs[best_idx]
    best_score = float(sims[best_idx])
    
    obligation_keywords = auto_keywords.get(obligation, [])
    keyword_hits = [kw for kw in obligation_keywords if kw.lower() in best_doc.page_content.lower()]
    keyword_ratio = len(keyword_hits) / max(1, len(obligation_keywords))
    
    # Cosine Similarity Only for Confidence
    confidence = round(best_score * 100, 1)
    
    # Generic Principle-Based Prompt
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
- CRITICAL: "Secure licenses", "procure rights", "obtain permissions" mean CONTINUED USE (not termination) → These are acceptable alternatives to modification
- CRITICAL: "Reimburse", "refund", "credit" are TERMINATION options (customer gets money back and stops using the product)
- If the obligation requires "continued use", "replace", or "secure rights", and the clause offers "reimburse/refund/credit" as an alternative, this is a material deviation → NO
- Example: Obligation requires "secure continued use OR replace". Clause offers "secure rights OR substitute OR reimburse". The "reimburse" option allows termination instead of continued use → NO

**Discretion**: Discretion about HOW to achieve a result ≠ discretion about WHETHER to achieve it
- Example: "Vendor chooses remedy method (fix, license, replace)" = discretion on HOW → YES
- Example: "Vendor may provide support if deemed reasonable" = discretion on WHETHER → NO
- CRITICAL: If the clause says "at vendor's sole discretion" but provides multiple remedy options (e.g., "modify OR secure licenses"), the vendor MUST act - they just choose which method → This is discretion on HOW, not WHETHER → YES
- CRITICAL: Look for the COMMITMENT to achieve the result. If the clause commits to achieving the outcome (e.g., "ensure continued use", "remedy infringement"), the discretion is only about the method
- Example: "Vendor may, at its sole discretion, implement modifications OR secure licenses to ensure continued use" → Vendor MUST ensure continued use (commitment), discretion is only on method (modify vs. license) → YES

**Standard Exceptions**: Legal/regulatory carve-outs are acceptable for POSITIVE obligations
- Example: "keep confidential UNLESS required by law" = standard exception → YES
- Example: "not liable for damages EXCEPT gross negligence" = standard exception → YES
- Example: "keep confidential UNLESS needed for business purposes" = broad exception → NO

**Negative Obligations (Exclusions)**: If the obligation says vendor is "NOT liable" or "does not have to" do something, analyze carefully:
- The PURPOSE is to EXCLUDE vendor liability in specific scenarios
- If the clause adds "unless" or "except" conditions, ask: Do these conditions RE-IMPOSE the liability the obligation sought to exclude?
- If YES (the exceptions re-impose liability), return "No" - the exceptions negate the exclusion
- CONCRETE EXAMPLE: 
  - Obligation: "Vendor does not have to indemnify Bank if infringement is solely from Bank's unauthorized modification."
  - Clause: "Vendor has no obligation UNLESS: (1) modification was required by license, (2) modification was required by documentation, (3) modification was mutually agreed."
  - Analysis: These "unless" exceptions RE-IMPOSE indemnification liability for common scenarios (modifications required by docs, etc.), negating the exclusion → "No"
- The key question: Do the exceptions make the vendor liable again for scenarios the obligation said they should NOT be liable for? If yes → "No"

**Scope**: Broad exceptions that negate "all" or "any" = material conflict
- Example: "return ALL info EXCEPT for business, legal, disaster recovery" = negates "ALL" → NO
- Example: "indemnify EXCEPT customer modifications" = standard carve-out → YES

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "Explain the legal effect and whether it matches the obligation's purpose",
  "suggestion": "If 'No', suggest specific language to achieve compliance. If 'Yes', return null."
}}

Obligation:
{obligation}

Relevant Clauses:
{chr(10).join([d.page_content for d in docs])}
"""
    logger.debug(f"Generated Prompt for '{obligation[:50]}...': {prompt[:500]}...")

    llm_status, llm_reason = "No", ""
    try:
        # Chain-of-Thought Analysis with GPT-4o-mini
        cot_prompt = f"""
{prompt}

IMPORTANT: Before providing your final JSON answer, you MUST think step-by-step:

Step 1: What is the EXACT purpose of the obligation? (What outcome does it seek?)
Step 2: What does the clause ACTUALLY say? (Summarize the legal effect)
Step 3: Do they match? (Does the clause achieve the same outcome?)
Step 4: Are there any material conflicts? (Does the clause negate or weaken the obligation?)
Step 5: CRITICAL CHECK - If the obligation requires "continued use", "replace", or "secure rights", does the clause offer "reimburse", "refund", or "credit" as an option? If YES, this is a TERMINATION option that conflicts with continued use → Answer must be "No"
Step 6: CRITICAL CHECK - If the clause says "at vendor's sole discretion", does it provide multiple remedy options (e.g., "modify OR secure licenses")? If YES, this is discretion on HOW (method), not WHETHER (outcome) → The vendor MUST act, they just choose the method → Answer should be "Yes" if the methods achieve the same outcome
Step 7: NEGATIVE OBLIGATION CHECK - If the obligation says "does NOT have to" or "NOT liable" or "no obligation", check if the clause has "unless" or "except" conditions. Ask: Do these conditions RE-IMPOSE the liability the obligation sought to EXCLUDE? If YES (the exceptions make vendor liable again for scenarios the obligation excluded) → Answer MUST be "No"

After completing these steps, provide your final JSON answer.
"""
        
        # Retry logic for LLM calls
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a meticulous contract compliance expert. Think step-by-step before answering."},
                        {"role": "user", "content": cot_prompt}
                    ],
                    temperature=0.0,  # Deterministic reasoning
                    seed=42,      # Fixed seed for reproducibility
                    max_tokens=800
                )
                res_text = resp.choices[0].message.content.strip()
                logger.info(f"LLM analysis completed for '{obligation[:50]}...' (attempt {attempt + 1})")
                logger.debug(f"LLM Response: {res_text}")
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"LLM call failed after {max_retries} attempts: {e}")
                    raise

        
        # Extract JSON from response
        if "```json" in res_text:
            json_text = res_text.split("```json")[1].split("```")[0]
        elif "```" in res_text:
            json_text = res_text.split("```")[1]
        else:
            json_text = res_text
            
        parsed = json.loads(json_text)
        llm_status = parsed.get("is_present", "No").strip()
        
        # Normalize to Title Case (Yes/No)
        if llm_status.lower() == "yes":
            llm_status = "Yes"
        elif llm_status.lower() == "no":
            llm_status = "No"
        
        # Enforce strict Yes/No
        if llm_status not in ["Yes", "No"]:
            llm_status = "No"
            
        llm_reason = parsed.get("reason", "").strip()
        llm_suggestion = parsed.get("suggestion", None)
        
        # Fix suggestion logic: null/None for Yes, actual suggestion for No
        if llm_status == "Yes":
            llm_suggestion = None
        elif not llm_suggestion or llm_suggestion == "null":
            llm_suggestion = "Consider adding explicit language to address this obligation."
        
        # Create fallback steps for backward compatibility
        cot_steps = create_fallback_steps(llm_status, llm_reason)
            
    except Exception as e:
        logger.error(f"Error parsing LLM response for '{obligation[:50]}...': {e}")
        llm_reason = "Reason could not be parsed from model response."
        llm_suggestion = "Could not generate suggestion due to error."
        cot_steps = create_fallback_steps("No", llm_reason)
    
    # Final Status based on LLM (Semantic Analysis)
    final_status = llm_status
    
    # Removed strict similarity threshold to allow LLM reasoning (semantic match) to prevail
    # even if cosine similarity is low due to vocabulary differences.

    # Generate supporting clauses with deduplication by page/line
    seen_locations = set()
    supporting_clauses = []
    
    for d in docs:
        page = d.metadata.get('page')
        line = d.metadata.get('line')
        location_key = (page, line)
        
        # Only add if we haven't seen this page/line combination
        if location_key not in seen_locations:
            clause_text = d.page_content[:250].strip()
            supporting_clauses.append(f"[Page {page} Line {line}] {clause_text}")
            seen_locations.add(location_key)
    
    return {
        "obligation": obligation, "is_present": final_status, "reason": llm_reason,
        "similarity_score": round(best_score, 3), "keyword_hits": keyword_hits,
        "confidence": confidence, "page": best_doc.metadata.get("page"), "line": best_doc.metadata.get("line"),
        "supporting_clauses": supporting_clauses,
        "suggestion": llm_suggestion,
        "cot_steps": cot_steps  # NEW: Step-by-step validation results
    }

def analyze_contract(obligations_file_bytes, obligations_filename, contract_file_bytes, contract_filename, session_id):
    # 1. Load Obligations
    import io
    if obligations_filename.endswith(".csv"):
        df_ob = pd.read_csv(io.BytesIO(obligations_file_bytes)).dropna(how="all")
    else:
        df_ob = pd.read_excel(io.BytesIO(obligations_file_bytes)).dropna(how="all")
    
    df_ob.columns = [str(c).strip() for c in df_ob.columns]
    
    # Translate obligations
    df_ob["Language"] = df_ob.iloc[:, 0].astype(str).apply(lambda x: detect_language(x))
    df_ob["Obligation_English"] = df_ob.iloc[:, 0].astype(str).apply(lambda x: translate_to_english(x).strip())
    df_ob = df_ob[df_ob["Obligation_English"].str.strip() != ""].reset_index(drop=True)
    obligations = df_ob["Obligation_English"].tolist()
    
    # 2. Extract Contract Text
    if contract_filename.endswith(".pdf"):
        records = extract_text_from_pdf(contract_file_bytes)
    elif contract_filename.endswith(".docx"):
        records = extract_text_from_docx(contract_file_bytes)
    elif contract_filename.endswith(".xlsx"):
        records = extract_text_from_excel(contract_file_bytes)
    else:
        records = extract_text_from_txt(contract_file_bytes)
        
    # Translate contract text
    for rec in records:
        rec["text"] = translate_to_english(rec["text"]).strip()
        
    # 3. Build Vector Store
    docs = chunk_text(records)
    vector_path = get_user_vector_path(session_id)
    vs = build_vector_store(docs, vector_path)
    
    # 4. Generate Keywords
    auto_keywords = generate_dynamic_keywords(obligations)
    
    # 5. Run Analysis
    results = []
    for ob in obligations:
        results.append(query_rag(vs, ob, auto_keywords))
        
    # Cleanup vector store to prevent disk bloat
    try:
        shutil.rmtree(vector_path)
        logger.info(f"Cleaned up vector store: {vector_path}")
    except Exception as e:
        logger.warning(f"Failed to cleanup vector store {vector_path}: {e}")
    
    # 6. Prepare Full Text for Preview Fallback
    full_text = "\n\n".join([r["text"] for r in records])

    return results, full_text