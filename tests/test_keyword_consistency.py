"""
Test script to verify keyword generation consistency.
This script tests that keywords are generated consistently across multiple runs.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import generate_dynamic_keywords, _keyword_cache, KEYWORD_CACHE_FILE

def test_keyword_consistency():
    """Test that keywords are consistent across multiple runs."""
    
    test_obligations = [
        "Vendor must fix any defects within 30 days",
        "Customer is not liable for indirect damages",
        "Vendor must indemnify customer against IP infringement"
    ]
    
    print("=" * 80)
    print("KEYWORD GENERATION CONSISTENCY TEST")
    print("=" * 80)
    print()
    
    # Clear cache to start fresh
    if os.path.exists(KEYWORD_CACHE_FILE):
        os.remove(KEYWORD_CACHE_FILE)
        print("✓ Cleared existing keyword cache")
    
    # First run - should generate keywords
    print("\n--- RUN 1: Generating keywords (should call LLM) ---")
    keywords_run1 = generate_dynamic_keywords(test_obligations)
    
    for ob, kws in keywords_run1.items():
        print(f"\nObligation: {ob}")
        print(f"Keywords ({len(kws)}): {', '.join(kws[:10])}...")
    
    # Second run - should use cache
    print("\n--- RUN 2: Generating keywords (should use cache) ---")
    keywords_run2 = generate_dynamic_keywords(test_obligations)
    
    # Compare results
    print("\n--- COMPARISON ---")
    all_match = True
    for ob in test_obligations:
        kws1 = keywords_run1[ob]
        kws2 = keywords_run2[ob]
        match = kws1 == kws2
        all_match = all_match and match
        
        status = "✓ MATCH" if match else "✗ MISMATCH"
        print(f"\n{status}: {ob[:50]}...")
        if not match:
            print(f"  Run 1: {kws1}")
            print(f"  Run 2: {kws2}")
    
    print("\n" + "=" * 80)
    if all_match:
        print("✓ SUCCESS: All keywords are consistent across runs!")
    else:
        print("✗ FAILURE: Keywords are inconsistent!")
    print("=" * 80)
    
    return all_match

if __name__ == "__main__":
    success = test_keyword_consistency()
    sys.exit(0 if success else 1)
