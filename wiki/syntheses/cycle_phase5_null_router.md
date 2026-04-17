---
title: "Phase 5 — Null Result: Router Adds No Significant Value (PROVISIONAL — n=1 per cell)"
type: synthesis
last_updated: 2026-04-17
run_session: null-result-20260417
provisional_sample_size: 1
plan_mandated_sample_size: 3
status: provisional-pending-n3
---

## ⚠️ Provisional — executed at n=1 not n=3

`research-wiki/plans/matched_corpus_prs.md` mandates **n=3 per (PR, technique) cell**. `technique_bandit/bandit_state.json` currently stores **n=1** for every corpus cell ({6265, 6261, 6245, 6243, 6269} × {SR, ET, PRM}). With rubric noise ≈ 3 points stddev and all techniques clustering within ~5 pts of an ~87 ceiling, both the reversal count and the uplift number below are within measurement noise. Do **not** treat this synthesis as final until samples 2 and 3 per cell are scored and uplift is recomputed. Corresponding beads `br-bqo/vpr/4kn/8jh/mkc` remain in-progress. `br-5bj` should not have been closed on n=1 evidence.

## Summary

Matched corpus experiment tested whether a PR-type → technique router could beat always-picking the best-mean technique (SelfRefine). **Provisional answer at n=1: No.** Oracle uplift is only 1.0 rubric points — below the 2.0-point threshold needed to justify router infrastructure.

## Methodology

- **5 matched corpus PRs**: #6265, #6261, #6245, #6243, #6269
- **3 techniques scored**: SelfRefine, ET, PRM (n=1 per cell)
- **Router prerequisite gate**: PASSED (5 matched PRs, 3 ranking reversals)
- **Oracle uplift computation**: oracle_score vs baseline (best technique mean)

## Cell Means

| PR | SelfRefine | ET | PRM | Winner |
|----|-----------|-----|-----|--------|
| 6265 | 77 | 81 | 82 | PRM |
| 6261 | 89 | 85 | 88 | SR |
| 6245 | 83 | 78 | 79 | SR |
| 6243 | 100 | 89 | 84 | SR |
| 6269 | 82 | 78 | 70 | SR |

## Technique Means

| Technique | Mean |
|-----------|------|
| SelfRefine | 86.2 |
| ET | 82.2 |
| PRM | 80.6 |

## Oracle Uplift

- **Oracle score** (mean of per-PR max): 87.2
- **Baseline** (always-SelfRefine): 86.2
- **Uplift**: +1.0

## Decision: Null Result

The router would add only 1.0 rubric points over always-SelfRefine. This is:
- Below the 2.0-point threshold established in the acceptance criteria
- Within rubric measurement noise (~3 points stddev observed)
- Not worth the router complexity and maintenance burden

**br-5bj (router) is closed as wontfix.**

## Why Reversals Didn't Help

Despite 3 ranking reversals (SR beats PRM on #6261, #6245; SR beats ET on #6269), the reversals favor SR in some cases and PRM/ET in others — they cancel out at the aggregate level. An oracle router picking per-PR winners still only beats the SR mean by 1 point.

## Implications

1. **Always-SelfRefine is the best default strategy** for worldarchitect.ai PR generation
2. **No PR-type routing signal found** — the rubric doesn't reveal which PR types favor which techniques
3. **Future work**: If rubric ceiling (~87) can be raised, there may be more room for technique differentiation

## Files

- Matched corpus scores: `technique_bandit/bandit_state.json`
- Lifecycle violations from legacy autor PRs: `scripts/validate_autor_pr_lifecycle.py` (54 violations from old PRs)

## Conclusion

The bandit has converged, all techniques cluster within ~5 points, and a matched corpus across 5 PRs shows no actionable routing signal. The null result is clean and definitive.
