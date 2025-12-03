"""
Script to restore backend/core.py from git repository
"""
import subprocess
import os

os.chdir(r"c:\Users\m.potnuru\Downloads\training_docs\python_install\my_repos\RAG\ContractAnalysisPlatform_v3_enhanced_genric_prompt_working_Copy")

# Try to restore the file using git checkout
try:
    # First, check git status
    result = subprocess.run(
        ["powershell", "-Command", "Get-Content .git/HEAD"],
        capture_output=True,
        text=True
    )
    print("Git HEAD:", result.stdout)
    
    # Try to restore the file
    result = subprocess.run(
        ["powershell", "-Command", "python -c \"import subprocess; subprocess.run(['git', 'checkout', 'HEAD', 'backend/core.py'])\""],
        capture_output=True,
        text=True,
        shell=True
    )
    print("Restore result:", result.stdout)
    print("Restore errors:", result.stderr)
    
except Exception as e:
    print(f"Error: {e}")
    
# Alternative: Try to read the git object directly
print("\nAttempting to find git objects...")
try:
    result = subprocess.run(
        ["powershell", "-Command", "Get-ChildItem .git/objects -Recurse -File | Select-Object -First 10 FullName"],
        capture_output=True,
        text=True
    )
    print("Git objects:", result.stdout)
except Exception as e:
    print(f"Error listing objects: {e}")
