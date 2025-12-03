"""
Safe script to strengthen the prompt by adding MANDATORY PRE-CHECKS section
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the beginning of the prompt to add MANDATORY PRE-CHECKS
old_start = """    prompt = f\"\"\"
You are a contract compliance analyst. Analyze whether the contract clause satisfies the obligation.

CRITICAL: Focus on LEGAL EFFECT and COMMERCIAL OUTCOME, not exact wording."""

new_start = """    prompt = f\"\"\"
You are a contract compliance analyst. Analyze whether the contract clause satisfies the obligation.

CRITICAL: Focus on LEGAL EFFECT and COMMERCIAL OUTCOME, not exact wording.

MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):
1. ⚠️ TERMINATION CHECK: If the obligation requires "continued use", "replace", or "secure rights", does the clause offer "reimburse", "refund", or "credit"? If YES → STOP → Answer is "No" (termination ≠ continued use)
2. ⚠️ NEGATIVE OBLIGATION CHECK: If the obligation says "does NOT have to", "NOT liable", or "no obligation", does the clause have "unless/except" conditions that RE-IMPOSE the excluded liability? If YES → STOP → Answer is "No" (exceptions negate the exclusion)

If EITHER pre-check triggers, your answer MUST be "No". Only proceed to full analysis if both pre-checks pass."""

if old_start in content:
    content = content.replace(old_start, new_start)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SUCCESS! Added MANDATORY PRE-CHECKS section to prompt")
    print("\nThis will force the LLM to check for:")
    print("1. Termination options (reimburse/refund/credit) when obligation requires continued use")
    print("2. Unless/except conditions that re-impose liability for negative obligations")
    print("\nThese checks happen BEFORE any other analysis")
else:
    print("❌ Could not find the expected text")
    print("Searching for alternative location...")
