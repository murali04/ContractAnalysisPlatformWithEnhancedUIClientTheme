"""
Quick dry run test with GPT-4o for the 4 user obligations
"""

import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Test cases - the 4 user obligations
test_cases = [
    {
        "name": "Obligation 1: Confidential Info Return",
        "obligation": "vendor agrees to return all confidential information and data to bank in format acceptable to bank.",
        "clause": "The receiving Party shall follow the disclosing party's reasonable instructions regarding the handling and disposal. However, return or destruction is not required for confidential information that must be retained for a) valid business purpose b) submission to government authority c) disaster recovery requirement d) technology the receiving party is permitted to retain under section 27.0. The receiving party may also retain one copy if required by applicable law.",
        "expected": "No"
    },
    {
        "name": "Obligation 2: Indemnity Exclusion",
        "obligation": "Vendor does not have to indemnify the Bank if the infringement is solely from Bank's unauthorized modification or use of the product.",
        "clause": "ABC shall have no obligation with respect to any claim arising solely from: a) a modification of any product by customer, or b) any combination of such product with a non-ABC product, unless: 1) The modification or combination is required under the applicable license 2) The modification or combination is required by ABC product documentation 3) The combination constitutes an essential element of the patent claim, or 4) The modification or combination is mutually agreed in writing by the parties.",
        "expected": "No"
    },
    {
        "name": "Obligation 3: Remedy for Infringement",
        "obligation": "Vendor shall undertake all necessary modifications the product to full remedy any infringement, without degradation of the product.",
        "clause": "Vendor shall retain the exclusive right, at its sole discretion and employing all reasonable commercial efforts, to implement such modifications, alterations, or adjustments to the affected portion of the service as may be necessary to render that portion non-infringing under applicable law. Furthermore, vendor may, in lieu of such modification, secure and maintain - at vendor sole cost and expense - all rights, licenses, consents, or permissions required to ensure that subscriber may continue to access, utilize, and benefit from the affected portion of the services without interruption.",
        "expected": "Yes"
    },
    {
        "name": "Obligation 4: IP Warranty (Refund Escape)",
        "obligation": "The Licensee must guarantee that Licensed Products do not infringe patents or copyrights; if they do, the Licensee must (i) secure continued use rights, (ii) replace with non-infringing products.",
        "clause": "The Licensee hereby warrants that all Licensed Products shall be free from any infringement. In the event any such claim arises, the Licensee shall, at its sole cost and expense, promptly procure the necessary rights or licenses to continue lawful use of the Licensed Products, substitute them with non-infringing equivalents of comparable quality, or reimburse purchasers in full for the affected goods.",
        "expected": "No"
    },
]

prompt_template = """
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
- The clause narrows the obligation in a way that excludes common scenarios
- The clause adds conditions that re-impose obligations the original sought to exclude

Key Principles:

**Alternative Remedies**: Multiple paths to the same outcome = compliant
- "Secure licenses", "procure rights" mean CONTINUED USE (acceptable alternatives)
- "Reimburse", "refund", "credit" mean TERMINATION of use (material deviation if obligation requires continued use)

**Discretion**: Discretion about HOW ≠ discretion about WHETHER
- Focus on the COMMITMENT, not the discretion on method

**Standard Exceptions**: Legal/regulatory carve-outs are acceptable
- For negative obligations (exclusions), business exceptions that re-impose liability = "No"

**Scope**: Broad exceptions that negate "all" or "any" = material conflict

IMPORTANT: Think step-by-step:
Step 1: What is the EXACT purpose of the obligation?
Step 2: What does the clause ACTUALLY say?
Step 3: Do they match?
Step 4: Any material conflicts?

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "Explain the legal effect and whether it matches the obligation's purpose"
}}

Obligation: {obligation}

Clause: {clause}
"""

print("=" * 80)
print("DRY RUN TEST - GPT-4o")
print("=" * 80)
print()

passed = 0
failed = 0

for test in test_cases:
    prompt = prompt_template.format(
        obligation=test["obligation"],
        clause=test["clause"]
    )
    
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a meticulous contract compliance expert. Think step-by-step."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.05,
            max_tokens=600
        )
        
        res_text = resp.choices[0].message.content.strip()
        
        # Extract JSON
        if "```json" in res_text:
            json_text = res_text.split("```json")[1].split("```")[0]
        elif "```" in res_text:
            json_text = res_text.split("```")[1]
        else:
            json_text = res_text
            
        parsed = json.loads(json_text)
        actual = parsed.get("is_present", "No").strip()
        reason = parsed.get("reason", "").strip()
        
        # Normalize
        if actual.lower() == "yes":
            actual = "Yes"
        elif actual.lower() == "no":
            actual = "No"
        
        status = "[PASS]" if actual == test["expected"] else "[FAIL]"
        print(f"{status} | {test['name']}")
        print(f"   Expected: {test['expected']} | Actual: {actual}")
        print(f"   Reason: {reason[:150]}...")
        print()
        
        if actual == test["expected"]:
            passed += 1
        else:
            failed += 1
            
    except Exception as e:
        print(f"[ERROR] | {test['name']}: {e}")
        print()
        failed += 1

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print(f"Success Rate: {(passed / len(test_cases)) * 100:.1f}%")
print("=" * 80)
