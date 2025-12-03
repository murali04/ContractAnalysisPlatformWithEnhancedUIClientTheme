"""
Script to improve consistency by adding seed and hardening prompt
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add seed parameter to client.chat.completions.create
if 'temperature=0.0,  # Deterministic reasoning' in content:
    content = content.replace(
        'temperature=0.0,  # Deterministic reasoning',
        'temperature=0.0,  # Deterministic reasoning\n            seed=42,      # Fixed seed for reproducibility'
    )
    print("✅ Added seed parameter")

# 2. Move MANDATORY PRE-CHECKS to System Message (conceptually)
# Actually, let's keep it in the prompt but make it even more forceful by wrapping it in a special block
# and explicitly telling the model to output which check triggered if any.

old_precheck = """MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):
1. ⚠️ TERMINATION CHECK: If the obligation EXPLICITLY requires "continued use", "ensure access", or "maintain availability" as the PRIMARY outcome, does the clause offer "reimburse", "refund", or "credit" as an alternative remedy? If YES → STOP → Answer is "No" (termination ≠ continued use)
   - NOTE: This check applies ONLY when the obligation's PRIMARY purpose is continued use/access, NOT when "secure rights" is mentioned as a METHOD to achieve another goal (e.g., remedy infringement)
2. ⚠️ NEGATIVE OBLIGATION CHECK: If the obligation says "does NOT have to", "NOT liable", or "no obligation", does the clause have "unless/except" conditions that RE-IMPOSE the excluded liability? If YES → STOP → Answer is "No" (exceptions negate the exclusion)

If EITHER pre-check triggers, your answer MUST be "No". Only proceed to full analysis if both pre-checks pass."""

new_precheck = """MANDATORY PRE-CHECKS (Check these FIRST before any other analysis):

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

INSTRUCTION: If ANY pre-check fails, stop immediately and return "No". Do not over-analyze."""

if old_precheck in content:
    content = content.replace(old_precheck, new_precheck)
    print("✅ Refined MANDATORY PRE-CHECKS formatting")
else:
    print("⚠️ Could not find exact pre-check text to replace - might have been modified already")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nUpdates applied to improve consistency.")
