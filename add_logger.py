"""
Safe script to add logger to core.py
"""
import os

file_path = r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy\backend\core.py"

# Read the file
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in file: {len(lines)}")

# Find the line with "# Setup logging" and add logger after it
for i, line in enumerate(lines):
    if '# Setup logging' in line:
        print(f"\nFound '# Setup logging' at line {i+1}")
        # Check if logger already exists
        if i+2 < len(lines) and 'logger = logging.getLogger' in lines[i+2]:
            print("Logger already defined, no changes needed")
            break
        else:
            # Add logger after "load_dotenv()"
            # Find load_dotenv line
            for j in range(i, min(i+5, len(lines))):
                if 'load_dotenv()' in lines[j]:
                    print(f"Found 'load_dotenv()' at line {j+1}")
                    # Insert logger after this line
                    lines.insert(j+1, 'logger = logging.getLogger(__name__)\r\n')
                    print(f"✓ Added logger at line {j+2}")
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    
                    print(f"\n✅ SUCCESS! File now has {len(lines)} lines")
                    break
            break
else:
    print("\n❌ Could not find '# Setup logging' line")
