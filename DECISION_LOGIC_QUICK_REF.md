# LLM Decision Logic - Quick Reference

## Decision Flow Chart

```
┌─────────────────────────────────────────────────────────────┐
│  START: Obligation + Retrieved Contract Clauses            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1-2: Analysis (Always PASS)                          │
│  • Identify obligation purpose                             │
│  • Analyze clause effect                                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3: Match Analysis                                    │
│  Does clause achieve same outcome as obligation?           │
└────────────┬───────────────────────┬────────────────────────┘
             │ PASS                  │ FAIL
             ▼                       ▼
         Continue              ┌──────────┐
                              │ RESULT:  │
                              │   NO ❌   │
                              └──────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4: Material Conflicts Check                          │
│  Any material differences that change business value?      │
└────────────┬───────────────────────┬────────────────────────┘
             │ PASS                  │ FAIL
             ▼                       ▼
         Continue              ┌──────────┐
                              │ RESULT:  │
                              │   NO ❌   │
                              └──────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5: CRITICAL - Termination Check                      │
│  If obligation requires "continued use":                   │
│  Does clause offer "refund/reimburse/credit"?              │
└────────────┬───────────────────────┬────────────────────────┘
             │ PASS/N/A              │ FAIL
             ▼                       ▼
         Continue              ┌──────────┐
                              │ RESULT:  │
                              │   NO ❌   │
                              └──────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 6: CRITICAL - Discretion Check                       │
│  If clause has discretion language:                        │
│  Is it discretion on HOW (method) or WHETHER (outcome)?    │
└────────────┬───────────────────────┬────────────────────────┘
             │ PASS/N/A              │ FAIL
             ▼                       ▼
         Continue              ┌──────────┐
                              │ RESULT:  │
                              │   NO ❌   │
                              └──────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 7: CRITICAL - Negative Obligation Check              │
│  If obligation is negative ("does NOT have to"):           │
│  Do exceptions RE-IMPOSE the excluded liability?           │
└────────────┬───────────────────────┬────────────────────────┘
             │ PASS/N/A              │ FAIL
             ▼                       ▼
         Continue              ┌──────────┐
                              │ RESULT:  │
                              │   NO ❌   │
                              └──────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULT: YES ✅                           │
│  All checks passed - obligation is present in contract     │
└─────────────────────────────────────────────────────────────┘
```

## Key Decision Rules

### 🔴 Automatic NO Triggers
Any ONE of these causes immediate NO:
- ❌ Step 3 FAIL: Clause doesn't achieve same outcome
- ❌ Step 4 FAIL: Material conflicts exist
- ❌ Step 5 FAIL: Termination option when continued use required (CRITICAL)
- ❌ Step 6 FAIL: Discretion on WHETHER, not HOW (CRITICAL)
- ❌ Step 7 FAIL: Exceptions re-impose excluded liability (CRITICAL)

### 🟢 YES Condition
ALL of these must be true:
- ✅ Steps 3-4: PASS (clause matches and no material conflicts)
- ✅ Steps 5-7: PASS or N/A (all critical checks pass or not applicable)

## Step Categories

### 📊 Analysis Steps (1-4)
**Purpose**: Understand and compare
- Steps 1-2: Always PASS (just analysis)
- Steps 3-4: Can PASS/FAIL based on match quality

### 🚨 Critical Pre-Checks (5-7)
**Purpose**: Catch fundamental conflicts
- Must be PASS or N/A
- ONE FAIL = Automatic NO
- These are "deal-breakers"

## Example Scenarios

### Scenario A: Perfect Match ✅
```
Step 1: ✅ PASS - Analyzed purpose
Step 2: ✅ PASS - Analyzed effect
Step 3: ✅ PASS - Clause matches obligation
Step 4: ✅ PASS - No material conflicts
Step 5: ✅ PASS - No termination options
Step 6: ✅ PASS - Discretion on HOW
Step 7: ⊘ N/A  - Positive obligation
→ RESULT: YES ✅
```

### Scenario B: Termination Conflict ❌
```
Step 1: ✅ PASS - Analyzed purpose
Step 2: ✅ PASS - Analyzed effect
Step 3: ⚠️ WARNING - Partial match
Step 4: ⚠️ WARNING - Some conflicts
Step 5: ❌ FAIL - Has refund option (CRITICAL)
Step 6: ✅ PASS - Discretion on HOW
Step 7: ⊘ N/A  - Positive obligation
→ RESULT: NO ❌ (Failed critical step 5)
```

### Scenario C: No Match ❌
```
Step 1: ✅ PASS - Analyzed purpose
Step 2: ✅ PASS - Analyzed effect
Step 3: ❌ FAIL - Clause doesn't match
Step 4: ❌ FAIL - Material conflicts
Step 5: ⊘ N/A  - Not applicable
Step 6: ⊘ N/A  - Not applicable
Step 7: ⊘ N/A  - Positive obligation
→ RESULT: NO ❌ (Failed steps 3 & 4)
```

### Scenario D: Negative Obligation Conflict ❌
```
Step 1: ✅ PASS - Analyzed purpose
Step 2: ✅ PASS - Analyzed effect
Step 3: ⚠️ WARNING - Partial match
Step 4: ❌ FAIL - Material conflicts
Step 5: ⊘ N/A  - Not applicable
Step 6: ⊘ N/A  - Not applicable
Step 7: ❌ FAIL - Exceptions re-impose liability (CRITICAL)
→ RESULT: NO ❌ (Failed critical step 7)
```

## What Changes with Enhancement?

### Before (Current):
```
Input → LLM → Output: {"is_present": "No", "reason": "..."}
```
**You see**: Final answer only
**You don't see**: Which step failed

### After (Enhanced):
```
Input → LLM → Output: {
  "steps": [
    {"step": 1, "status": "PASS", ...},
    {"step": 2, "status": "PASS", ...},
    {"step": 3, "status": "PASS", ...},
    {"step": 4, "status": "PASS", ...},
    {"step": 5, "status": "FAIL", ...},  ← You can see this!
    {"step": 6, "status": "PASS", ...},
    {"step": 7, "status": "N/A", ...}
  ],
  "is_present": "No",
  "reason": "Failed critical step 5"
}
```
**You see**: Exactly which step failed and why
**Benefit**: Full transparency into the decision

## Summary

**Current System**: 
- LLM thinks through 7 steps internally
- Returns only final Yes/No
- Like a black box 📦

**Enhanced System**:
- LLM still thinks through 7 steps
- Returns result of EACH step
- Like a glass box 🔍

**Decision Logic**: Same in both cases
- Critical step fails → NO
- Analysis step fails → NO
- All pass → YES

**What's Different**: Visibility, not logic
