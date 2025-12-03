"""
Safe script to add Step 7 for negative obligations check
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the location to add Step 7 (after Step 6, before "After completing these steps")
old_text = """Step 6: CRITICAL CHECK - If the clause says "at vendor's sole discretion", does it provide multiple remedy options (e.g., "modify OR secure licenses")? If YES, this is discretion on HOW (method), not WHETHER (outcome) → The vendor MUST act, they just choose the method → Answer should be "Yes" if the methods achieve the same outcome

After completing these steps, provide your final JSON answer."""

new_text = """Step 6: CRITICAL CHECK - If the clause says "at vendor's sole discretion", does it provide multiple remedy options (e.g., "modify OR secure licenses")? If YES, this is discretion on HOW (method), not WHETHER (outcome) → The vendor MUST act, they just choose the method → Answer should be "Yes" if the methods achieve the same outcome
Step 7: NEGATIVE OBLIGATION CHECK - If the obligation says "does NOT have to" or "NOT liable" or "no obligation", check if the clause has "unless" or "except" conditions. Ask: Do these conditions RE-IMPOSE the liability the obligation sought to EXCLUDE? If YES (the exceptions make vendor liable again for scenarios the obligation excluded) → Answer MUST be "No"

After completing these steps, provide your final JSON answer."""

if old_text in content:
    content = content.replace(old_text, new_text)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ SUCCESS! Added Step 7 for negative obligations check")
    print("\nStep 7: NEGATIVE OBLIGATION CHECK - If the obligation says \"does NOT have to\"")
    print("or \"NOT liable\" or \"no obligation\", check if the clause has \"unless\" or \"except\"")
    print("conditions. Ask: Do these conditions RE-IMPOSE the liability the obligation sought")
    print("to EXCLUDE? If YES → Answer MUST be \"No\"")
else:
    print("❌ Could not find the expected text to replace")
    print("The file may have been modified or the text doesn't match exactly")
