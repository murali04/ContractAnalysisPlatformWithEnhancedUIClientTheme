"""
Comprehensive Test Suite for Contract Analysis Prompt
Tests various edge cases, scenarios, and contract types to verify:
1. Prompt is generic (not overfitted)
2. No hardcoded logic
3. Handles edge cases correctly
"""
import os
import sys
import logging
from dotenv import load_dotenv

sys.path.append(os.path.join(os.getcwd(), 'backend'))
from backend.core import build_vector_store, query_rag, chunk_text, generate_dynamic_keywords

logging.basicConfig(level=logging.WARNING)  # Reduce noise
load_dotenv()

# Test Categories
test_cases = {
    "TERMINATION_VS_CONTINUED_USE": [
        {
            "name": "Reimburse as escape (should be No)",
            "obligation": "Vendor must ensure continued use of the software without interruption",
            "clause": "In case of defects, vendor may at its option repair the software or refund the license fee",
            "expected": "No",
            "reason": "Refund is termination, not continued use"
        },
        {
            "name": "Replace with equivalent (should be Yes)",
            "obligation": "Vendor must ensure continued access to the service",
            "clause": "If service becomes unavailable, vendor shall provide substitute service of equal functionality",
            "expected": "Yes",
            "reason": "Substitute maintains continued access"
        },
        {
            "name": "Credit option mixed with fix (should be No)",
            "obligation": "Licensee must secure continued use rights if product infringes",
            "clause": "Licensee may procure licenses for continued use, or issue credit to customer",
            "expected": "No",
            "reason": "Credit is termination option"
        }
    ],
    
    "NEGATIVE_OBLIGATIONS": [
        {
            "name": "Simple exclusion (should be Yes)",
            "obligation": "Vendor is not liable for indirect damages",
            "clause": "Vendor shall not be liable for any indirect, incidental, or consequential damages",
            "expected": "Yes",
            "reason": "Clause matches exclusion"
        },
        {
            "name": "Exclusion with broad exceptions (should be No)",
            "obligation": "Vendor has no obligation to provide support for customer modifications",
            "clause": "Vendor has no support obligation, except where modification was recommended by vendor or required by vendor documentation",
            "expected": "No",
            "reason": "Exceptions re-impose support obligation"
        },
        {
            "name": "Exclusion with narrow exception (should be Yes)",
            "obligation": "Provider not liable for data loss",
            "clause": "Provider not liable for data loss except in cases of gross negligence or willful misconduct",
            "expected": "Yes",
            "reason": "Standard legal exception, doesn't negate exclusion"
        }
    ],
    
    "DISCRETION_HOW_VS_WHETHER": [
        {
            "name": "Discretion on method (should be Yes)",
            "obligation": "Vendor must remedy security vulnerabilities",
            "clause": "Vendor shall, at its discretion, patch the vulnerability or implement compensating controls",
            "expected": "Yes",
            "reason": "Discretion on HOW (patch vs controls), vendor MUST remedy"
        },
        {
            "name": "Discretion on whether to act (should be No)",
            "obligation": "Vendor must provide technical support",
            "clause": "Vendor may provide technical support if it deems the request reasonable",
            "expected": "No",
            "reason": "Discretion on WHETHER to provide support"
        },
        {
            "name": "Sole discretion with commitment (should be Yes)",
            "obligation": "Supplier must ensure regulatory compliance",
            "clause": "Supplier shall, in its sole discretion, modify products or obtain necessary approvals to ensure compliance",
            "expected": "Yes",
            "reason": "MUST ensure compliance, discretion only on method"
        }
    ],
    
    "ALTERNATIVE_REMEDIES": [
        {
            "name": "Multiple equivalent paths (should be Yes)",
            "obligation": "Contractor must prevent unauthorized access",
            "clause": "Contractor shall implement encryption or multi-factor authentication to prevent unauthorized access",
            "expected": "Yes",
            "reason": "Both achieve same outcome (prevent access)"
        },
        {
            "name": "Alternatives with different outcomes (should be No)",
            "obligation": "Developer must maintain system availability",
            "clause": "Developer shall restore system within 4 hours or provide full refund",
            "expected": "No",
            "reason": "Restore ≠ refund (different outcomes)"
        }
    ],
    
    "SCOPE_AND_EXCEPTIONS": [
        {
            "name": "Broad exception negating 'all' (should be No)",
            "obligation": "Company must delete all customer data upon termination",
            "clause": "Company shall delete all data except data needed for legal, audit, or business continuity purposes",
            "expected": "No",
            "reason": "Broad exceptions negate 'all'"
        },
        {
            "name": "Narrow standard exception (should be Yes)",
            "obligation": "Party must keep information confidential",
            "clause": "Party shall maintain confidentiality except as required by law or court order",
            "expected": "Yes",
            "reason": "Standard legal exception"
        }
    ],
    
    "MATERIALITY_TEST": [
        {
            "name": "Immaterial difference (should be Yes)",
            "obligation": "Vendor must respond to critical issues within 2 hours",
            "clause": "Vendor shall respond to severity 1 incidents within 2 hours",
            "expected": "Yes",
            "reason": "'Critical' and 'severity 1' are equivalent"
        },
        {
            "name": "Material difference in scope (should be No)",
            "obligation": "Provider must backup all data daily",
            "clause": "Provider shall backup production databases daily",
            "expected": "No",
            "reason": "'All data' ≠ 'production databases only'"
        }
    ],
    
    "DIFFERENT_WORDING_SAME_EFFECT": [
        {
            "name": "Different words, same legal effect (should be Yes)",
            "obligation": "Licensee must indemnify licensor against IP claims",
            "clause": "Licensee shall defend and hold harmless licensor from intellectual property infringement allegations",
            "expected": "Yes",
            "reason": "'Indemnify' = 'defend and hold harmless'"
        },
        {
            "name": "Similar words, different effect (should be No)",
            "obligation": "Vendor must guarantee 99.9% uptime",
            "clause": "Vendor shall use reasonable efforts to maintain 99.9% availability",
            "expected": "No",
            "reason": "'Guarantee' ≠ 'reasonable efforts' (different commitment levels)"
        }
    ]
}

def run_comprehensive_tests():
    print("=" * 120)
    print("COMPREHENSIVE CONTRACT ANALYSIS PROMPT TEST SUITE")
    print("=" * 120)
    print("\nTesting prompt generalization across multiple scenarios and edge cases")
    print("This verifies the prompt is NOT overfitted and handles various contract types\n")
    
    total_tests = sum(len(cases) for cases in test_cases.values())
    passed = 0
    failed = 0
    failed_tests = []
    
    for category, cases in test_cases.items():
        print(f"\n{'='*120}")
        print(f"CATEGORY: {category}")
        print(f"{'='*120}")
        
        for i, test in enumerate(cases, 1):
            # Prepare test
            records = [{"page": 1, "line": 1, "text": test["clause"]}]
            vs_path = f"temp_test_{category}_{i}"
            docs = chunk_text(records)
            vs = build_vector_store(docs, vs_path)
            auto_keywords = generate_dynamic_keywords([test["obligation"]])
            
            # Run analysis
            result = query_rag(vs, test["obligation"], auto_keywords)
            actual = result["is_present"]
            expected = test["expected"]
            match = actual == expected
            
            # Display result
            status = "✅ PASS" if match else "❌ FAIL"
            print(f"\n{i}. {test['name']}")
            print(f"   Obligation: {test['obligation'][:80]}...")
            print(f"   Clause: {test['clause'][:80]}...")
            print(f"   Expected: {expected} | Actual: {actual} | {status}")
            print(f"   Reason: {test['reason']}")
            
            if match:
                passed += 1
            else:
                failed += 1
                failed_tests.append({
                    "category": category,
                    "name": test["name"],
                    "expected": expected,
                    "actual": actual,
                    "llm_reason": result["reason"]
                })
                print(f"   ⚠️ LLM Reason: {result['reason'][:100]}...")
            
            # Cleanup
            import shutil
            if os.path.exists(vs_path):
                shutil.rmtree(vs_path)
    
    # Summary
    print(f"\n{'='*120}")
    print(f"TEST SUMMARY")
    print(f"{'='*120}")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed} ({passed/total_tests*100:.1f}%)")
    print(f"Failed: {failed} ({failed/total_tests*100:.1f}%)")
    
    if failed > 0:
        print(f"\n{'='*120}")
        print(f"FAILED TESTS DETAILS")
        print(f"{'='*120}")
        for ft in failed_tests:
            print(f"\n❌ {ft['category']}: {ft['name']}")
            print(f"   Expected: {ft['expected']} | Actual: {ft['actual']}")
            print(f"   LLM Reason: {ft['llm_reason']}")
    
    # Analysis
    print(f"\n{'='*120}")
    print(f"PROMPT GENERALIZATION ANALYSIS")
    print(f"{'='*120}")
    
    if passed / total_tests >= 0.85:
        print("✅ EXCELLENT: Prompt demonstrates strong generalization (≥85% pass rate)")
        print("   The prompt is NOT overfitted and handles diverse scenarios well")
    elif passed / total_tests >= 0.70:
        print("⚠️ GOOD: Prompt shows reasonable generalization (70-85% pass rate)")
        print("   Some edge cases may need refinement")
    else:
        print("❌ NEEDS IMPROVEMENT: Prompt may be overfitted (<70% pass rate)")
        print("   Significant refinement needed for edge cases")
    
    print(f"\n{'='*120}")
    
    return passed == total_tests

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
