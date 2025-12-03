"""
Test obligation 2 specifically to understand why it's returning Yes instead of No
"""
import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.getcwd(), 'backend'))
from backend.core import build_vector_store, query_rag, chunk_text, generate_dynamic_keywords

logging.basicConfig(level=logging.INFO)
load_dotenv()

# Obligation 2 - Negative obligation (exclusion)
ob2 = "Vendor does not have to indemnify the Bank if the infringement is solely from Bank's unauthorized modification or use of the product."

# Contract clause 2
contract2 = """Vendor shall defend customer and its affiliates against any claim to the extent it alleges that a product, fix or services deliverable made available by ABC for a fee and used within the scope of the license misappropriates a trade secret or infringes a patent, copyright, trademark, or other proprietary right of a third party. ABC's obligations under this section apply solely to clams of direct infringement. For covered products, ABC's defense and payment obligations are further subject to customer copyright commitment under the product terms. Notwithstanding the foregoing, ABC shall have no obligation with respect to any claim arising solely form: a) a modification of any product, fix, or deliverable by customer, or b) any combination of such product, fix, or deliverable with a non-ABC product, unless: 1) The modification or combination is required under the applicable license 1. The modification or combination is required by ABC product documentation 2. The combination of an ABC production with a non-ABC product constitutes an essential or inventive element of the patent claim, or 3. The modification or combination is mutually agreed in writing by the parties ABC's defense obligations apply only to customers or its affiliates using the P Products, fixes or deliverables as permitted in a supplemental agreement. Further, ABC shall have no obligation where a claim is asserted against an affiliate that is no using products, fixes or deliverables."""

print("="*100)
print("TESTING OBLIGATION 2 (Negative Obligation)")
print("="*100)
print(f"\nObligation: {ob2}")
print(f"\nExpected Result: No")
print(f"\nReason: The clause has 'unless' exceptions that RE-IMPOSE indemnification liability")
print("  - unless (1) modification required by license")
print("  - unless (2) modification required by documentation")  
print("  - unless (3) mutually agreed")
print("\nThese exceptions negate the exclusion because they make vendor liable again")
print("for common scenarios (modifications required by docs, etc.)")
print("\n" + "="*100)

# Prepare and test
records = [{"page": 1, "line": 1, "text": contract2}]
vs_path = "temp_ob2_vs"
docs = chunk_text(records)
vs = build_vector_store(docs, vs_path)
auto_keywords = generate_dynamic_keywords([ob2])

result = query_rag(vs, ob2, auto_keywords)

print(f"\nActual Result: {result['is_present']}")
print(f"Confidence: {result['confidence']}")
print(f"Similarity Score: {result['similarity_score']}")
print(f"\nReason: {result['reason']}")
print(f"\nSuggestion: {result.get('suggestion', 'N/A')}")

print("\n" + "="*100)
if result['is_present'] == "No":
    print("✅ CORRECT - Obligation 2 correctly identified as No")
else:
    print("❌ INCORRECT - Obligation 2 should be No, but got Yes")
    print("\nThe prompt needs to better handle negative obligations with 'unless' exceptions")
print("="*100)

# Cleanup
import shutil
if os.path.exists(vs_path):
    shutil.rmtree(vs_path)
