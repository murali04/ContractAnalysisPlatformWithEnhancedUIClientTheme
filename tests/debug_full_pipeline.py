
import os
import sys
import json
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from openai import OpenAI
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
embedder = OpenAIEmbeddings(model="text-embedding-3-small")

# 1. Reconstruct Contract Text (from User Logs)
contract_text_page_1 = """
Vendor shall defend customer and its affiliates against any claim to the extent
it alleges that a product, fix or services deliverable made available by ABC for a fee and used
within the scope of the license misappropriates a trade secret or infringes a patent, copyright,
trademark, or other proprietary right of a third party. ABC's obligations under this section apply
solely to clams of direct infringement. For covered products, ABC's defense and payment
obligations are further subject to customer copyright commitment under the product terms.
Notwithstanding the foregoing, ABC shall have no obligation with respect to any claim arising
solely form:
a) a modification of any product, fix, or deliverable by customer, or
b) any combination of such product, fix, or deliverable with a non-ABC product, unless:
1) The modification or combination is required under the applicable license       
1. The modification or combination is required by ABC product documentation       
2. The combination of an ABC production with a non-ABC product constitutes an essential or
inventive element of the patent claim, or
3.  The modification or combination is mutually agreed in writing by the parties  
ABC's defense obligations apply only to customers or its affiliates using the P Products, fixes or
deliverables as permitted in a supplemental agreement. Further, ABC shall have no obligation where a
claim is asserted against an affiliate that is no using products, fixes or deliverables.
"""

# 2. Mock Backend Functions (Replicating core.py logic)

def chunk_text_mock(text):
    # Replicating the FIX: Group by page (we only have 1 page here)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = []
    chunks = splitter.split_text(text)
    for idx, chunk in enumerate(chunks):
        docs.append(Document(
            page_content=chunk, 
            metadata={"page": 1, "line": "n/a", "chunk_id": idx}
        ))
    return docs

def build_vector_store_mock(docs):
    vs = FAISS.from_documents(docs, embedder)
    return vs

def generate_keywords_mock(obligation):
    # Replicating Hybrid Strategy
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a legal search expert. Return a JSON object with a key 'keywords' containing 5-8 search terms for the given obligation. \n\nCRITICAL: You must predict the **exact words** a vendor would use to **limit** or **avoid** this obligation.\n- Example: If obligation is 'fix', search for 'refund', 'credit', 'obsolescence'.\n- Example: If obligation is 'indemnify', search for 'defend', 'hold harmless', 'control of defense'.\n- Example: If obligation is 'unlimited', search for 'cap', 'aggregate liability', 'fees paid'.\n\nFocus on specific nouns and verbs found in the contract text."},
                {"role": "user", "content": obligation}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        res_text = response.choices[0].message.content
        parsed = json.loads(res_text)
        keywords = parsed.get("keywords", [])
        
        universal_danger_words = ["refund", "reimburse", "terminate", "cap", "limit", "sole discretion", "exclusive remedy", "unless", "except"]
        keywords.extend(universal_danger_words)
        return list(set(keywords))
    except Exception as e:
        print(f"Keyword Gen Error: {e}")
        return ["refund", "reimburse", "terminate", "cap", "limit", "unless", "except"]

def query_rag_mock(vs, obligation, keywords):
    # Retrieval
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    docs = retriever.get_relevant_documents(obligation)
    
    # Keyword Filtering (Simulated)
    # In core.py we don't strictly filter, we just use keywords to boost confidence or for debug.
    # But let's check if keywords are actually in the docs
    print("\n--- RETRIEVED CHUNKS ---")
    for i, d in enumerate(docs):
        print(f"Chunk {i+1}: {d.page_content[:100]}...")
        
    # Prompt Construction (Exact copy from core.py)
    prompt = f"""
You are a multilingual contract compliance analyst. Translate internally to English.
Analyze the obligation and the relevant clauses. Return valid JSON ONLY.

Task: Determine if the 'Obligation' is fully present and agreed to in the 'Relevant Clauses'.

Guidelines:
1. **Substantial Compliance**: Focus on the *legal effect* rather than exact wording. If the Relevant Clauses achieve the same commercial or legal result as the Obligation, return "Yes".
   - *Example*: "Reasonable commercial efforts" is usually acceptable for obligations requiring a result, unless the obligation explicitly demands an absolute guarantee.
   - *Example*: If an obligation requires "fixing" a defect, but the clause allows "securing rights" (licensing) to ensure continued use, this is compliant ("Yes").

2. **Standard Exceptions**: Accept standard legal carve-outs (e.g., "disclosure required by law" for confidentiality, "force majeure") as compliant, unless the Obligation explicitly forbids them.

3. **Material Deviation**: Return "No" ONLY if the Relevant Clauses contain a **material conflict** that significantly weakens or negates the Obligation.
   - *Example*: If Obligation asks for "Unlimited Liability" and Clause sets a "Cap", this is a material conflict ("No").
   - *Example*: If Obligation asks for "Net 30" payment and Clause says "Net 45", this is a material conflict ("No").
   - *Example (CRITICAL)*: If Obligation requires "Fix or Replace" (implying continued use), and Clause adds a "Refund" or "Reimburse" option that allows the vendor to terminate use, this is a material conflict ("No").

4. **Negative Obligations (Exclusions)**: If the Obligation states the Vendor is *NOT* liable for X (an exclusion), but the Relevant Clauses add "exceptions" or "carve-outs" where the Vendor *IS* liable, this is a material conflict ("No").
   - *Example*: Obligation: "Vendor not liable for any modifications." Clause: "Vendor not liable for modifications UNLESS required by documentation." -> Result: "No" (The exception re-imposes liability).
   - *CRITICAL*: Look for words like "unless", "except", "subject to", "provided that". If these introduce conditions where the vendor IS liable, return "No".

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "short 1-2 sentence rationale",
  "suggestion": "If 'No', provide a specific clause suggestion to add or modify to achieve compliance. If 'Yes', return null."
}}

Obligation:
{obligation}

Relevant Clauses:
{chr(10).join([d.page_content for d in docs])}
"""
    print("\n--- GENERATED PROMPT ---")
    print(prompt)
    
    # LLM Call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a concise contract compliance expert who replies in JSON. You only output Yes or No."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=400
    )
    res_text = response.choices[0].message.content.strip()
    print("\n--- LLM RESPONSE ---")
    print(res_text)
    return res_text

# 3. Run the Pipeline
if __name__ == "__main__":
    obligation = "Vendor does not have to indemnify the Bank if the infringement is solely from Bank's unauthorized modification or use of the product."
    
    print(f"Analyzing Obligation: {obligation}")
    
    # Step 1: Chunk
    docs = chunk_text_mock(contract_text_page_1)
    print(f"Created {len(docs)} chunks.")
    
    # Step 2: Vector Store
    vs = build_vector_store_mock(docs)
    
    # Step 3: Keywords
    keywords = generate_keywords_mock(obligation)
    print(f"Generated Keywords: {keywords}")
    
    # Step 4: Query & Analyze
    query_rag_mock(vs, obligation, keywords)
