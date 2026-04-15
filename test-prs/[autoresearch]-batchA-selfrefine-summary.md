---
title: "SelfRefine Study Batch A Summary"
type: test-summary
technique: SelfRefine
batch: A
date: 2026-04-15
---

## Summary Table

| PR | Score | Diff Similarity | Key Finding |
|----|-------|----------------|-------------|
| 6212 | 88/100 | 75% | Correctly identified launch guard + scrubbing logic |
| 6214 | 86/100 | 70% | Predicted followup deletion; missed generic synthesis |
| 6218 | 72/100 | 45% | Confused with PR 6214; underestimated infrastructure addition |

## Overall Results

- **Mean Score**: 82/100
- **Mean Diff Similarity**: 63%

## Key Findings

### 1. SelfRefine Works Well for Bug Fixes
PR 6212 (launch CTA + atomicity) was a concrete bug fix. The technique correctly identified:
- Frontend state guard (`isLaunching`)
- Backend scrubbing logic (replacing `pass`)

### 2. Optimization PRs Are Harder
PR 6214 (remove followup LLM call) was an optimization. We missed:
- The generic (non-level-up) synthesis path
- Two-phase postcondition pattern
- Sentinel class removal

### 3. Infrastructure PRs Require More Context
PR 6218 adds functions that PR 6214 depends on, but we didn't have that context in iteration 1.

## What Worked

- Reading the PR summary carefully
- Identifying key files and functions
- Iteration-by-iteration refinement

## What Didn't Work

- Not having full diff context in iteration 1
- Missing cross-PR dependencies
- Underestimating test coverage needs

## Recommendations

1. **For optimization PRs**: Study the old code path first before predicting the new one
2. **For infrastructure PRs**: Check what dependent PRs exist
3. **Always predict test changes**: They reveal interface expectations