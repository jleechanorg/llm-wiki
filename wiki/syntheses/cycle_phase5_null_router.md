---
title: "Phase 5 — Null Result: Router Adds No Significant Value (n=3 CONFIRMED)"
type: synthesis
last_updated: 2026-04-18
run_session: matched-corpus-n3-20260418
provisional_sample_size: 1
plan_mandated_sample_size: 3
status: definitive-null
---

## Definitive Result — n=3 per cell confirmed

All 30 remaining scoring runs completed (samples 2 and 3 per cell). Oracle uplift at n=3: **0.93** — well below the 2.0-point threshold. The null result is confirmed.

## Summary

Matched corpus experiment tested whether a PR-type → technique router could beat always-picking the best-mean technique (SelfRefine). **Answer: No.** Oracle uplift is only 0.93 rubric points — well below the 2.0-point threshold needed to justify router infrastructure. br-5bj (router) remains closed as wontfix.

## Methodology

- **5 matched corpus PRs**: #6265, #6261, #6245, #6243, #6269
- **3 techniques scored**: SelfRefine, ET, PRM (n=3 per cell = 45 total runs)
- **Router prerequisite gate**: PASSED (5 matched PRs, 3 ranking reversals)
- **Oracle uplift computation**: oracle_score vs baseline (best technique mean)

## Cell Means (n=3)

| PR | SelfRefine | ET | PRM | Winner | Notes |
|----|-----------|-----|-----|--------|-------|
| 6265 | 79.25 | 78.58 | 82.08 | PRM | |
| 6261 | 80.17 | 80.38 | 79.33 | ET | |
| 6245 | 76.73 | 74.92 | 78.32 | PRM | |
| 6243 | 97.08 | 91.42 | 87.50 | SR | SR dominates on this small semantic change |
| 6269 | 72.92 | 71.58 | 68.33 | SR | SR least bad on interface-port PR |

## Technique Means

| Technique | n | Mean |
|-----------|---|------|
| SelfRefine | 15 | 81.23 |
| ET | 15 | 79.38 |
| PRM | 15 | 79.11 |

## Oracle Uplift

- **Oracle score** (mean of per-PR max): 82.16
- **Baseline** (always-SelfRefine): 81.23
- **Uplift**: +0.93

## Decision: Null Result (Definitive)

The router would add only 0.93 rubric points over always-SelfRefine. This is:
- Below the 2.0-point threshold established in the acceptance criteria
- Within rubric measurement noise (~3 points stddev observed)
- Not worth the router complexity and maintenance burden

**br-5bj (router) is closed as wontfix.**

## Why Reversals Didn't Help

3 ranking reversals exist (PRM > SR on #6265; ET > SR on #6261; PRM > SR on #6245), but they cancel at the aggregate. The oracle router picking per-PR winners still only beats the SR mean by 0.93 points. No consistent PR-type → technique mapping emerges.

## Implications

1. **Always-SelfRefine is the best default strategy** for worldarchitect.ai PR generation
2. **No PR-type routing signal found** — the rubric doesn't reveal which PR types favor which techniques
3. **Techniques cluster tightly**: SR 81.23, ET 79.38, PRM 79.11 — all within 2.1 points
4. **Future work**: If rubric ceiling (~87) can be raised, there may be more room for technique differentiation

## Score Artifacts

30 new score JSONs committed:
- `research-wiki/scores/SR_<pr>_s2_<ts>.json`
- `research-wiki/scores/SR_<pr>_s3_<ts>.json`
- `research-wiki/scores/ET_<pr>_s2_<ts>.json`
- `research-wiki/scores/ET_<pr>_s3_<ts>.json`
- `research-wiki/scores/PRM_<pr>_s2_<ts>.json`
- `research-wiki/scores/PRM_<pr>_s3_<ts>.json`

Run session: `matched-corpus-n3-20260418`

## Conclusion

At n=3 per cell (45 total runs), the null result holds. A PR-type → technique router adds only 0.93 points over always-SelfRefine — well within rubric noise. The bandit has converged and all three techniques cluster within 2.1 rubric points. The router bead br-5bj is correctly closed as wontfix.
