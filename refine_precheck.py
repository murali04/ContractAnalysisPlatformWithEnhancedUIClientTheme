"""
Script to refine MANDATORY PRE-CHECK #1 to be more precise
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the pre-check to be more precise
old_precheck = """MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):
1. ⚠️ TERMINATION CHECK: If the obligation requires "continued use", "replace", or "secure rights", does the clause offer "reimburse", "refund", or "credit"? If YES → STOP → Answer is "No" (termination ≠ continued use)
2. ⚠️ NEGATIVE OBLIGATION CHECK: If the obligation says "does NOT have to", "NOT liable", or "no obligation", does the clause have "unless/except" conditions that RE-IMPOSE the excluded liability? If YES → STOP → Answer is "No" (exceptions negate the exclusion)

If EITHER pre-check triggers, your answer MUST be "No". Only proceed to full analysis if both pre-checks pass."""

new_precheck = """MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):
1. ⚠️ TERMINATION CHECK: If the obligation EXPLICITLY requires "continued use", "ensure access", or "maintain availability" as the PRIMARY outcome, does the clause offer "reimburse", "refund", or "credit" as an alternative remedy? If YES → STOP → Answer is "No" (termination ≠ continued use)
   - NOTE: This check applies ONLY when the obligation's PRIMARY purpose is continued use/access, NOT when "secure rights" is mentioned as a METHOD to achieve another goal (e.g., remedy infringement)
2. ⚠️ NEGATIVE OBLIGATION CHECK: If the obligation says "does NOT have to", "NOT liable", or "no obligation", does the clause have "unless/except" conditions that RE-IMPOSE the excluded liability? If YES → STOP → Answer is "No" (exceptions negate the exclusion)

If EITHER pre-check triggers, your answer MUST be "No". Only proceed to full analysis if both pre-checks pass."""

if old_precheck in content:
    content = content.replace(old_precheck, new_precheck)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SUCCESS! Refined MANDATORY PRE-CHECK #1")
    print("\nKey change:")
    print("- Pre-check now only triggers when 'continued use' is the PRIMARY outcome")
    print("- Does NOT trigger when 'secure rights' is a METHOD to achieve another goal")
    print("\nThis fixes Obligation 3 (remedy infringement) while keeping Obligation 4 (continued use) correct")
else:
    print("❌ Could not find the expected text")
