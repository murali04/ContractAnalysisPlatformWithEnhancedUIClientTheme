"""
Safe script to replace debug print statements with logger.debug calls
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

# Make replacements
changes_made = []

# Line 274 (index 273)
if len(lines) > 273:
    original_274 = lines[273]
    print(f"\nLine 274 original: {original_274.strip()}")
    if 'print("DEBUG: Generated Prompt:' in original_274:
        lines[273] = '    # print("DEBUG: Generated Prompt:\\n", prompt) # Debugging line - COMMENTED OUT\r\n'
        lines.insert(274, '    logger.debug(f"Generated Prompt: {prompt}")\r\n')
        changes_made.append("Line 274: Commented print and added logger.debug")
        print("✓ Line 274 replaced")
    else:
        print("✗ Line 274 doesn't match expected content")

# Line 303 (now 304 after insert, originally index 302)
# Need to find it dynamically since line numbers shifted
for i, line in enumerate(lines):
    if 'print("DEBUG: LLM Response:' in line:
        print(f"\nFound LLM Response print at line {i+1}: {line.strip()}")
        lines[i] = '        # print("DEBUG: LLM Response:\\n", res_text) # Debugging line - COMMENTED OUT\r\n'
        lines.insert(i+1, '        logger.debug(f"LLM Response: {res_text}")\r\n')
        changes_made.append(f"Line {i+1}: Commented print and added logger.debug")
        print(f"✓ Line {i+1} replaced")
        break

if changes_made:
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"\n✅ SUCCESS! Made {len(changes_made)} changes:")
    for change in changes_made:
        print(f"  - {change}")
    print(f"\nNew file has {len(lines)} lines")
else:
    print("\n❌ No changes made - couldn't find expected lines")
