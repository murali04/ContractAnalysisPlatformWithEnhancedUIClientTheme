
import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Add parent directory to path to allow imports if needed, though we are using direct OpenAI call here
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def test_prompt(obligation, relevant_clauses):
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
   - *CRITICAL*: If the clause contains words like "unless", "except", "subject to", "provided that", it introduces a condition. For a negative obligation (exclusion), ANY condition is a material conflict. Return "No".

Return JSON:
{{
  "is_present": "Yes" or "No",
  "reason": "short 1-2 sentence rationale",
  "suggestion": "If 'No', provide a specific clause suggestion to add or modify to achieve compliance. If 'Yes', return null."
}}

Obligation:
{obligation}

Relevant Clauses:
{relevant_clauses}
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
        return json.loads(res_text)
    except Exception as e:
        return {"error": str(e)}

test_cases = [
    {
        "category": "Confidentiality (Standard)",
        "obligation": "The Receiver must hold all Confidential Information in strict confidence and not disclose it to any third party.",
        "clause": "The Recipient agrees to protect the Confidential Information with the same degree of care it uses to protect its own confidential information. The Recipient may disclose Confidential Information if required by law.",
        "expected": "Yes"
    },
    {
        "category": "Payment Terms (Mismatch)",
        "obligation": "Payment shall be made within 30 days of the invoice date.",
        "clause": "Customer shall pay all undisputed amounts within forty-five (45) days of receipt of the applicable invoice.",
        "expected": "No"
    },
    {
        "category": "Liability Cap (Conflict)",
        "obligation": "The Vendor's liability for data breaches shall be unlimited.",
        "clause": "In no event shall Vendor's aggregate liability arising out of or related to this Agreement exceed the total amount paid by Customer hereunder.",
        "expected": "No"
    },
    {
        "category": "Termination (Notice Period)",
        "obligation": "Either party may terminate this agreement with 30 days prior written notice.",
        "clause": "This Agreement may be terminated by either party for convenience upon providing sixty (60) days written notice to the other party.",
        "expected": "No" 
    },
    {
        "category": "Governing Law (Standard)",
        "obligation": "This Agreement shall be governed by the laws of the State of New York.",
        "clause": "This Agreement and any disputes arising out of it shall be governed by and construed in accordance with the laws of the State of California.",
        "expected": "No"
    },
    {
        "category": "Original Edge Case (Remedy)",
        "obligation": "Vendor must remedy any infringement claim by fixing the product or replacing it.",
        "clause": "Vendor will use reasonable commercial efforts to modify the software to be non-infringing. If Vendor cannot do so, Vendor may refund the fees paid and terminate the license.",
        "expected": "No" 
    },
    {
        "category": "Support Hours (Partial)",
        "obligation": "Vendor shall provide 24/7 technical support.",
        "clause": "Vendor provides support during standard business hours (9am-5pm EST), Monday through Friday.",
        "expected": "No"
    },
    {
        "category": "Data Location (Conflict)",
        "obligation": "All customer data must be stored within the European Union.",
        "clause": "Customer data may be processed and stored in the United States or any other country where Vendor operates.",
        "expected": "No"
    },
    {
        "category": "Audit Rights (Vague)",
        "obligation": "Customer has the right to audit Vendor's records once annually.",
        "clause": "Customer may audit Vendor's relevant records upon providing reasonable prior written notice.",
        "expected": "Yes"
    },
    {
        "category": "Insurance (Currency)",
        "obligation": "Vendor must maintain liability insurance of at least $5,000,000.",
        "clause": "Vendor shall maintain Commercial General Liability insurance with a limit of not less than $2,000,000 per occurrence.",
        "expected": "No"
    },
    {
        "category": "User Case 3 (Alt Remedy + Discretion)",
        "obligation": "Vendor shall undertake all necessary modifications the product to full remedy any infringement, without degradation of the product.",
        "clause": "Vendor shall retain the exclusive right, at its sole discretion and employing all reasonable commercial efforts, to implement such modifications, alterations, or adjustments to the affected portion of the service as may be necessary to render that portion non-infringing under applicable law. Furthermore, vendor may, in lieu of such modification, secure and maintain - at vendor sole cost and expense - all rights, licenses, consents, or permissions required to ensure that subscriber may continue to access, utilize, and benefit from the affected portion of the services without interruption. Such actions may be taken by vendor whenever it deems them reasonable necessary to mitigate or resolve any claim or threat of infringement.",
        "expected": "Yes"
    },
    {
        "category": "User Case 2 (Negative Obligation Exceptions)",
        "obligation": "Vendor does not have to indemnify the Bank if the infringement is solely from Bank's unauthorized modification or use of the product.",
        "clause": "Vendor shall defend customer... Notwithstanding the foregoing, ABC shall have no obligation with respect to any claim arising solely form: a) a modification of any product... by customer... unless: 1) The modification... is required under the applicable license 1. The modification or combination is required by ABC product documentation 2. The combination of an ABC production with a non-ABC product constitutes an essential or inventive element of the patent claim, or 3. The modification or combination is mutually agreed in writing by the parties",
        "expected": "No"
    },
    {
        "category": "User Case 4 (Refund Escape)",
        "obligation": "The Licensee must guarantee that Licensed Products do not infringe patents or copyrights; if they do, the Licensee must (i) secure continued use rights, (ii) replace with non-infringing products.",
        "clause": "The Licensee hereby warrants and represents that all Licensed Products shall be free from any infringement or misappropriation of third-party intellectual property rights, including but not limited to patents, copyrights, trademarks, or trade secrets. In the event any such claim or proceeding arises, the Licensee shall, at its sole cost and expense, promptly procure the necessary rights or licenses to continue lawful use of the Licensed Products, substitute them with non-infringing equivalents of comparable quality, or reimburse purchasers in full for the affected goods. Furthermore, the Licensee shall indemnify and hold harmless the Licensor from all losses, damages, and reasonable legal fees incurred in defending any such infringement action, regardless of its outcome.",
        "expected": "No"
    }
]

print(f"{'Category':<30} | {'Expected':<10} | {'Actual':<10} | {'Reason':<50}")
print("-" * 110)

for case in test_cases:
    result = test_prompt(case["obligation"], case["clause"])
    actual = result.get("is_present", "Error")
    reason = result.get("reason", "N/A")
    print(f"{case['category']:<30} | {case['expected']:<10} | {actual:<10} | {reason[:50]}...")
