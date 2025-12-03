"""
Simple test to check if obligations are working correctly
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Test with a simple direct call
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test obligation 3 which should return "Yes"
obligation = "Vendor shall undertake all necessary modifications the product to full remedy any infringement, without degradation of the product."
contract = """Vendor shall retain the exclusive right, at its sole discretion and employing all reasonable commercial efforts, to implement such modifications, alterations, or adjustments to the affected portion of the service as may be necessary to render that portion non-infringing under applicable law. Furthermore, vendor may, in lieu of such modification, secure and maintain - at vendor sole cost and expense - all rights, licenses, consents, or permissions required to ensure that subscriber may continue to access, utilize, and benefit from the affected portion of the services without interruption. Such actions may be taken by vendor whenever it deems them reasonable necessary to mitigate or resolve any claim or threat of infringement."""

print("Testing Obligation 3...")
print(f"Obligation: {obligation}")
print(f"\nContract: {contract}")
print("\n" + "="*80)

# Simple test without the full RAG pipeline
prompt = f"""
You are a contract compliance analyst. Analyze whether the contract clause satisfies the obligation.

CRITICAL: Focus on LEGAL EFFECT and COMMERCIAL OUTCOME, not exact wording.

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

Key Principles:

**Alternative Remedies**: Multiple paths to the same outcome = compliant
- Example: "modify OR secure licenses" both prevent infringement and ensure continued use → YES
- CRITICAL: "Secure licenses", "procure rights", "obtain permissions" mean CONTINUED USE (not termination)

**Discretion**: Discretion about HOW to achieve a result ≠ discretion about WHETHER to achieve it
- Example: "Vendor chooses remedy method (fix, license, replace)" = discretion on HOW → YES
- CRITICAL: If the clause says "at vendor's sole discretion" but provides multiple remedy options (e.g., "modify OR secure licenses"), the vendor MUST act - they just choose which method → This is discretion on HOW, not WHETHER → YES

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "Explain the legal effect and whether it matches the obligation's purpose"
}}

Obligation:
{obligation}

Relevant Clauses:
{contract}
"""

try:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a meticulous contract compliance expert. Think step-by-step before answering."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
        max_tokens=800
    )
    
    import json
    res_text = resp.choices[0].message.content.strip()
    print("LLM Response:")
    print(res_text)
    print("\n" + "="*80)
    
    # Extract JSON
    if "```json" in res_text:
        json_text = res_text.split("```json")[1].split("```")[0]
    elif "```" in res_text:
        json_text = res_text.split("```")[1]
    else:
        json_text = res_text
    
    parsed = json.loads(json_text)
    status = parsed.get("is_present", "No").strip()
    reason = parsed.get("reason", "")
    
    print(f"\nFinal Result:")
    print(f"Status: {status}")
    print(f"Reason: {reason}")
    print(f"\nExpected: Yes")
    print(f"Match: {'✅ PASS' if status == 'Yes' else '❌ FAIL'}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
