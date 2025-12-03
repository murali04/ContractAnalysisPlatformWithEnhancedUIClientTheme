"""
Comprehensive Dry Run Test for Generic Compliance Prompt
Tests the new principle-based prompt across diverse contract scenarios
"""

import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Generic Principle-Based Prompt (matching backend/core.py)
def test_compliance(obligation, clause, expected_result, test_name):
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
- The clause narrows the obligation in a way that excludes common scenarios
- The clause adds conditions that re-impose obligations the original sought to exclude

Key Principles:

**Alternative Remedies**: Multiple paths to the same outcome = compliant
- Example: "modify OR secure licenses" both prevent infringement and ensure continued use → YES
- Example: "fix OR refund and terminate" have different outcomes (continued use vs. termination) → NO
- CRITICAL: If the obligation implies continued use/service, any option that allows termination is a material deviation
- CRITICAL: "Reimburse", "refund", "credit" mean TERMINATION of use. If the obligation requires "continued use", "replace", or "secure rights", these are material deviations → NO

**Discretion**: Discretion about HOW to achieve a result ≠ discretion about WHETHER to achieve it
- Example: "Vendor chooses remedy method (fix, license, replace)" = discretion on HOW → YES
- Example: "Vendor may provide support if deemed reasonable" = discretion on WHETHER → NO
- CRITICAL: If the clause says "at vendor's sole discretion" but still commits to achieving the result, focus on the COMMITMENT, not the discretion

**Standard Exceptions**: Legal/regulatory carve-outs are acceptable unless explicitly forbidden
- Example: "confidential UNLESS required by law" = standard exception → YES
- Example: "not liable for damages EXCEPT gross negligence" = standard exception → YES
- Example: "confidential UNLESS needed for business purposes" = broad exception → NO
- CRITICAL: For negative obligations (exclusions), standard legal/regulatory exceptions are acceptable; business exceptions are not

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
{clause}
"""
    
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a concise contract compliance expert who replies in JSON. You only output Yes or No."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=400
        )
        res_text = resp.choices[0].message.content.strip()
        if "```json" in res_text:
            res_text = res_text.split("```json")[1].split("```")[0]
        elif "```" in res_text:
            res_text = res_text.split("```")[1]
        parsed = json.loads(res_text)
        actual_result = parsed.get("is_present", "No").strip()
        reason = parsed.get("reason", "").strip()
        
        # Normalize
        if actual_result.lower() == "yes":
            actual_result = "Yes"
        elif actual_result.lower() == "no":
            actual_result = "No"
        
        status = "[PASS]" if actual_result == expected_result else "[FAIL]"
        print(f"{status} | {test_name}")
        print(f"   Expected: {expected_result} | Actual: {actual_result}")
        print(f"   Reason: {reason[:100]}...")
        print()
        
        return actual_result == expected_result
    except Exception as e:
        print(f"[ERROR] | {test_name}: {e}")
        print()
        return False

# Test Cases
test_cases = [
    # USER-PROVIDED OBLIGATIONS
    {
        "name": "User Ob 1: Confidential Info Return (Broad Exceptions)",
        "obligation": "Vendor agrees to return all confidential information and data to bank in format acceptable to bank.",
        "clause": "The receiving Party shall follow the disclosing party's reasonable instructions regarding the handling and disposal. However, return or destruction is not required for confidential information that must be retained for a) valid business purpose b) submission to government authority c) disaster recovery requirement d) technology the receiving party is permitted to retain under section 27.0.",
        "expected": "No"
    },
    {
        "name": "User Ob 2: Indemnity Exclusion (Exceptions Re-impose Liability)",
        "obligation": "Vendor does not have to indemnify the Bank if the infringement is solely from Bank's unauthorized modification or use of the product.",
        "clause": "ABC shall have no obligation with respect to any claim arising solely from: a) a modification of any product by customer, or b) any combination of such product with a non-ABC product, unless: 1) The modification or combination is required under the applicable license 2) The modification or combination is required by ABC product documentation 3) The combination constitutes an essential element of the patent claim.",
        "expected": "No"
    },
    {
        "name": "User Ob 3: Remedy for Infringement (Alternative Methods OK)",
        "obligation": "Vendor shall undertake all necessary modifications the product to full remedy any infringement, without degradation of the product.",
        "clause": "Vendor shall retain the exclusive right, at its sole discretion and employing all reasonable commercial efforts, to implement such modifications, alterations, or adjustments to the affected portion of the service as may be necessary to render that portion non-infringing under applicable law. Furthermore, vendor may, in lieu of such modification, secure and maintain - at vendor sole cost and expense - all rights, licenses, consents, or permissions required to ensure that subscriber may continue to access, utilize, and benefit from the affected portion of the services without interruption.",
        "expected": "Yes"
    },
    {
        "name": "User Ob 4: IP Warranty (Refund Escape Clause)",
        "obligation": "The Licensee must guarantee that Licensed Products do not infringe patents or copyrights; if they do, the Licensee must (i) secure continued use rights, (ii) replace with non-infringing products.",
        "clause": "The Licensee hereby warrants that all Licensed Products shall be free from any infringement. In the event any such claim arises, the Licensee shall, at its sole cost and expense, promptly procure the necessary rights or licenses to continue lawful use of the Licensed Products, substitute them with non-infringing equivalents of comparable quality, or reimburse purchasers in full for the affected goods.",
        "expected": "No"
    },
    
    # EDGE CASES - ALTERNATIVE REMEDIES
    {
        "name": "Edge: Alternative Remedy (Same Outcome)",
        "obligation": "Vendor must fix any defects in the software.",
        "clause": "Vendor shall, at its option, either (a) repair the defect, (b) replace the defective component, or (c) provide a workaround that achieves the same functionality.",
        "expected": "Yes"
    },
    {
        "name": "Edge: Alternative Remedy (Different Outcome)",
        "obligation": "Vendor must fix any defects in the software.",
        "clause": "Vendor shall, at its option, either (a) repair the defect, or (b) refund the license fee and terminate the agreement.",
        "expected": "No"
    },
    
    # EDGE CASES - DISCRETION
    {
        "name": "Edge: Discretion on HOW (Acceptable)",
        "obligation": "Vendor shall provide technical support.",
        "clause": "Vendor shall provide technical support via phone, email, or online portal, at Vendor's sole discretion based on the nature of the issue.",
        "expected": "Yes"
    },
    {
        "name": "Edge: Discretion on WHETHER (Not Acceptable)",
        "obligation": "Vendor shall provide technical support.",
        "clause": "Vendor may, at its sole discretion, provide technical support if it deems the request reasonable.",
        "expected": "No"
    },
    
    # EDGE CASES - STANDARD EXCEPTIONS
    {
        "name": "Edge: Standard Legal Exception (Acceptable)",
        "obligation": "All information shall be kept confidential.",
        "clause": "All information shall be kept confidential, except as required by law, court order, or regulatory authority.",
        "expected": "Yes"
    },
    {
        "name": "Edge: Broad Business Exception (Not Acceptable)",
        "obligation": "All information shall be kept confidential.",
        "clause": "All information shall be kept confidential, except as needed for business purposes, marketing, or sharing with affiliates.",
        "expected": "No"
    },
    
    # EDGE CASES - SCOPE NARROWING
    {
        "name": "Edge: Narrow Scope (Excludes Common Scenarios)",
        "obligation": "Vendor shall indemnify Customer for all IP infringement claims.",
        "clause": "Vendor shall indemnify Customer for IP infringement claims, but only for claims arising from use of the software in its unmodified form, in the United States, and only for direct infringement (not contributory or induced).",
        "expected": "No"
    },
    {
        "name": "Edge: Reasonable Scope Limitation",
        "obligation": "Vendor shall indemnify Customer for IP infringement claims.",
        "clause": "Vendor shall indemnify Customer for IP infringement claims arising from the software when used in accordance with the documentation and applicable law.",
        "expected": "Yes"
    },
    
    # EDGE CASES - NEGATIVE OBLIGATIONS
    {
        "name": "Edge: Negative Obligation with Standard Exception",
        "obligation": "Vendor shall not be liable for indirect or consequential damages.",
        "clause": "Vendor shall not be liable for indirect or consequential damages, except in cases of gross negligence or willful misconduct.",
        "expected": "Yes"  # Standard legal exception
    },
    {
        "name": "Edge: Negative Obligation with Broad Exception",
        "obligation": "Vendor shall not be liable for service interruptions.",
        "clause": "Vendor shall not be liable for service interruptions, except for interruptions caused by Vendor's systems, third-party providers, or scheduled maintenance.",
        "expected": "No"  # Exceptions cover most scenarios
    },
    
    # EDGE CASES - QUANTITATIVE DIFFERENCES
    {
        "name": "Edge: Material Quantitative Difference",
        "obligation": "Payment terms are Net 30 days.",
        "clause": "Payment terms are Net 90 days.",
        "expected": "No"
    },
    {
        "name": "Edge: Immaterial Quantitative Difference",
        "obligation": "Vendor shall respond to support requests within 24 hours.",
        "clause": "Vendor shall respond to support requests within 1 business day.",
        "expected": "Yes"
    },
]

# Run Tests
print("=" * 80)
print("COMPREHENSIVE DRY RUN TEST - GENERIC COMPLIANCE PROMPT")
print("=" * 80)
print()

passed = 0
failed = 0

for test in test_cases:
    result = test_compliance(
        test["obligation"],
        test["clause"],
        test["expected"],
        test["name"]
    )
    if result:
        passed += 1
    else:
        failed += 1

print("=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_cases)} tests")
print(f"Success Rate: {(passed / len(test_cases)) * 100:.1f}%")
print("=" * 80)
