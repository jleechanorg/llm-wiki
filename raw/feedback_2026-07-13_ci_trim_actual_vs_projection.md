---
name: ci-trim-forward-projections-underestimate-cascade-effects-6-5x
description: "When projecting CI compute-hour savings from trigger-elimination trims, model cascade effects on downstream workflows — not just direct trigger reduction. Lane F's 37.86h/48h projection was 6.5x conservative vs actual 246.53h/48h measured 14h post-trim on worldarchitect.ai."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-792ix
  originSessionId: 6d6509e7-ea7b-44a2-8aa5-e0699e99ba2c
---

# CI trim forward projections underestimate cascade effects 6.5x

## Context
- 2026-07-13 round-6 re-measurement of worldarchitect.ai CI savings 14h after rounds 1-3 trim PRs landed
- Lane F's original 27.10h pre-trim measurement projected 37.86 compute-hr/48h savings
- Lane F2 re-measurement: actual is 246.53 compute-hr/48h — **6.5x larger than projected**
- Runs eliminated: projected −2,201/48h vs actual **−7,338/48h** (3.3x larger)

## Why Lane F's projection methodology was wrong
Lane F modeled "X% reduction in Y workflow" instead of "remove entire trigger category." The cascade effect — when `hermes-pr-tag-listener`'s `issue_comment` trigger is removed, downstream `MCP Smoke Tests` and `Auth Browser Tests` triggers that would have been caused by those events also stop — wasn't modeled.

## Per-PR actual vs projected deltas (round 6 measurement)
| PR | Workflow | LF Δcomp | Actual Δcomp | Verdict |
|---|---|---:|---:|---|
| #8363 (r2) | test.yml push trim | −3.32 | −62.99 | **19x larger** |
| #8270 (r1) | filter:blob:none → MCP Smoke | −0.84 | −12.76 | **15x larger** |
| #8270 (r1) | filter:blob:none → Auth Browser | −0.28 | −3.36 | **12x larger** |
| #8366 (r3) | mvp-shard1 sha-conc | −5.85 | −34.49 | 5.9x larger |
| #8365+#8368 (r3) | Green Gate | −17.30 | −59.63 | 3.4x larger |
| #8367 (r3) | Presubmit paths | −9.65 | −32.15 | 3.3x larger |

## Skip rate actually moved
- Baseline: 74.0% skip rate
- Lane F's projection: skip floor would NOT move (74.0% steady)
- Actual: 74.0% → 54.9% (moved 19pp)
- Why: the skip-driver workflows (high trigger counts) were the ones eliminated, so the remaining workflow mix has fewer naturally-skippable runs.

## Rule for future CI trim projections
- **Cascade model required**: when removing a trigger, account for downstream workflows that would have been triggered by those events.
- **Re-measurement is non-optional**: 14h+ post-trim data validated the projection was 6.5x conservative; without re-measurement, the under-projection would have persisted.
- **Skip rate CAN move**: don't assume it's a static floor; the workflows that drive skip-rate are the natural trim targets.
- **Trigger-elimination wins are multiplicative**: removing 100% of one trigger can cascade into 5-10x reduction on downstream workflows.

## References
- Re-measurement report: `/tmp/worldarchitect.ai/sidekick/round6-2026-07-13/lane-f2-remeasurement.md`
- Lane F original: `/tmp/worldarchitect.ai/sidekick/round4-2026-07-13/lane-f-measurement.md`
- Bead: `rev-792ix` (closed after 14h re-measurement)
- PRs: #8354, #8356, #8360, #8363, #8364, #8365, #8366, #8367, #8368, #8369, #8370, #8371, #8372, #8374
- Lane B pre-trim data at /tmp/gh_runs_round2_skip_breakdown/

## Verification
- Round 1-3 effectiveness: confirmed
- Round 4-5 follow-ups: PRs #8369, #8370 effective; PR #8371 (evidence-bundle variants) FAILED (failure rate went from 59% to 73%) — bead `rev-f08di` opened for round 7
- Cumulative compute savings landed: 246.53h/48h (vs Lane F projection 37.86h/48h)
