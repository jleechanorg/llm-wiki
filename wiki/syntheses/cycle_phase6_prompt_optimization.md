---
title: "Phase 6 — Prompt Optimization Within SelfRefine (V1: Null Result)"
type: synthesis
phase: 6
bead: br-1xk
status: "null-v1"
run_session: "phase6-v1-20260418"
date: 2026-04-18
---

## Executive Summary

**Result: NULL** — SR-v2 (rubric-targeted critique variant) did not achieve the +2.0 point acceptance criterion.

| Metric | Value |
|--------|-------|
| SR baseline mean | 81.23 |
| SR-v2 mean | 81.15 |
| Uplift | -0.08 |
| Target acceptance | ≥ +2.0 (need 83.23) |
| Status | NULL |

---

## Phase 6 V1: Rubric-Targeted Critique (SR-v2)

### Hypothesis

Replacing generic "improve this" self-critique with an explicit 6-dimension rubric-targeted critique would improve consistency, especially in often-weak dimensions like Documentation and Type Safety.

**Expected mechanism:**
- Baseline SR uses generic critique: "improve this implementation"
- SR-v2 uses structured critique: score each of 6 dimensions, then focus rewriting on the 2 lowest

### Design

**Critique prompt template (EXACT):**
```
Review this implementation against these criteria and score each 0-100:
1. Naming (15%): snake_case, descriptive, no abbreviations
2. Error Handling (20%): typed exceptions, no bare except, logged errors
3. Type Safety (20%): TypedDict for data shapes, explicit return types
4. Architecture (20%): follows existing patterns, single responsibility
5. Test Coverage (15%): covers happy path + edge cases + error paths
6. Documentation (10%): docstrings for public methods, inline for non-obvious

For the 2 lowest-scoring dimensions, rewrite the implementation to improve them.
Output: first the per-dimension scores, then the rewritten implementation.
```

**Execution:** 3 refinement rounds (same as baseline SR), 5 PRs × 3 runs = 15 evaluations.

### Results

Per-PR breakdown:

| PR | Baseline SR | SR-v2 | Δ |
|----|-------------|-------|---|
| 6265 | 79.25 | 80.78 | +1.53 |
| 6261 | 80.17 | 80.55 | +0.38 |
| 6245 | 76.73 | 82.42 | +5.69 ✓ |
| 6243 | 97.08 | 81.00 | -16.08 |
| 6269 | 72.92 | 81.02 | +8.10 ✓ |

**Aggregate:**
- SR-v2 beat baseline on 2 of 5 PRs (6245, 6269)
- SR-v2 significantly underperformed on 1 PR (6243, likely high variance)
- Mean: 81.15 vs baseline 81.23 → **-0.08 (null)**

### Why No Uplift?

Three candidate explanations:

1. **Rubric ceiling** — Both SR and SR-v2 converge around 80-82 because the rubric itself has a ceiling. The 6-dim rubric may not effectively discriminate between good and excellent code at this score range.

2. **Variance dominance** — PR-to-PR variance (72.92 to 97.08 baseline) dominates technique variance. The matched corpus includes 6243, which has an intrinsic high quality that both techniques "bottom out" on differently.

3. **Prompt saturation** — The base SR prompt is already near-optimal for this task. Adding rubric structure doesn't improve the LLM's reasoning; it may just constrain the solution space without benefit.

### Oracle Analysis

If a perfect selector could pick the best per-PR result from SR and SR-v2:
- Oracle mean: 84.37
- Baseline: 81.23
- **Potential uplift: +3.14**

This suggests that technique combination (ensemble) could work, but SR-v2 alone does not.

---

## Implications for Phase 7

### Option 1: Rubric + Content Co-Evolution
Rather than varying prompt alone, evolve both:
- The rubric dimensions themselves (add domain-specific dimensions?)
- The critique template (multi-stage critique with feedback loops?)
- The synthesis strategy (rank dimensions by PR type, not universally)

### Option 2: Technique Ensemble
Instead of picking a single best technique, design a voting scheme:
- Run multiple techniques (SR, ET, PRM, SR-v2, etc.)
- Aggregate or ensemble the results
- Expected uplift: ~+2-3 points based on oracle analysis

### Option 3: Acceptance Criteria Relaxation
The +2.0 bar was set before any variants were evaluated. Post-hoc analysis shows:
- All techniques converge 79-82 on matched corpus
- Variation within technique > variation between techniques
- Meaningful discrimination may require n > 3 or held-out corpus

---

## Null-Result Policy Compliance

Per Phase 6 plan:
> "If no variant beats SR-baseline+2 at n=3, write a null synthesis. Do NOT increase n past 3 to p-hack a winner."

**Compliance: YES**
- Evaluated SR-v2 at n=3 per cell (15 total runs)
- Result: null (-0.08 uplift)
- NOT p-hacking with increased n
- Proceeding to Phase 7 or closing experiment

---

## Artifacts

- Score JSONs: `research-wiki/scores/SR-v2_*`
- Logs: `wiki/syntheses/et_logs/SR-v2_*`
- Bandit state: `technique_bandit/bandit_state.json` (SR-v2 entries appended)
- Oracle uplift: tested with `scripts/oracle_uplift.py --techniques SR SR-v2`

---

## Conclusion

**SR-v2 (rubric-targeted critique) = NULL variant.**

The hypothesis that explicit rubric structure would improve critique quality was not supported. Both SR and SR-v2 converge to similar means, suggesting:
- The prompt variation alone is insufficient
- Technique-level levers may be exhausted
- Next phase should explore architectural/ensemble approaches

**Recommendation:** Move to Phase 7 (rubric + prompt co-evolution) or close Phase 6 as complete null-result experiment.
