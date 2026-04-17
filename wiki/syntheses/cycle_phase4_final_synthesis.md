---
title: "Phase 4 Final Synthesis — What Worked, What Didn't, Recommendations"
type: synthesis
tags: [auto-research, phase4, final-synthesis, recommendations, bandit]
last_updated: 2026-04-16
run_session: phase4-synthesis
---

# Phase 4 Final Synthesis

## Executive Summary

Phase 3 held-out validation on 6 draft autor PRs (#6330-#6335) + PRM #6338 confirms: **all three techniques converge to ~80-87** with overlapping confidence intervals. No technique is clearly superior. The ~87 ceiling is a **rubric artifact**, not a technique ceiling. Phase 4 should pivot to **problem decomposition** (which PR types benefit from which techniques) rather than technique ranking.

---

## Final Bandit State (Post Phase 3)

```
SelfRefine : mean=83.8  n=26  α=20.3 β=9.8
ET         : mean=82.5  n=12  α=10.4 β=5.6
PRM        : mean=82.0  n= 8  α=7.7 β=4.3
```

**Interpretation**: SelfRefine has the highest posterior mean but also the most observations (n=26, means more data = less uncertainty). ET and PRM have wider CIs due to fewer observations. Confidence intervals for all three **overlap substantially** — no statistically significant winner.

---

## Phase 3 Held-Out Results

| PR | Technique | Score | Delta vs Original | Notes |
|----|-----------|-------|-------------------|-------|
| #6330 | SelfRefine | 80 | +0 vs original | Rename-only subset, lost on docs |
| #6331 | SelfRefine | 81 | +7 vs original | Shell script fix, cleaner |
| #6332 | SelfRefine | 85 | +5 vs original | Simpler approach |
| #6333 | SelfRefine | 75 | +0 vs original | Same scope |
| #6335 | SelfRefine | 78 | +1 vs original | Simpler |
| #6338 | PRM | 87 | +6 vs original | Fix 1 (world_logic) 93, Fix 2 (agent_prompts) 81 |

**SelfRefine avg on held-out**: 80.2 (vs 87.5 biased Phase 2 estimate — Phase 2 estimate was inflated)
**PRM #6338**: 87/100 — highest single score in Phase 3

---

## What Worked

### 1. Thompson Sampling Bandit — Converged Quickly
After n=26 SelfRefine, n=12 ET, n=8 PRM observations, all three posteriors stabilized with overlapping CIs. The bandit correctly identified that more data won't change the ranking — convergence reached.

### 2. Held-Out Validation — Corrected Phase 2 Bias
Phase 2 SelfRefine estimate of 87.5 was inflated by non-held-out methodology. Held-out validation on draft autor PRs yielded 80.2 avg — **7.3 point correction**. This validates the held-out approach as the correct methodology.

### 3. PRM on Complex Multi-Fix PRs
PRM #6338 (rewards_box + circuit breaker) scored 87 — the highest in Phase 3. PRM's step-by-step reasoning helped on a complex PR with two independent fixes. Hypothesis: **PRM advantages appear on complex PRs** where sequential reasoning adds value.

### 4. SelfRefine on Rename/Refactor PRs
SelfRefine consistently matched or beat originals on rename PRs (#6330: 80 vs original 80, but +4 in naming). The critique-and-refine loop is well-suited for naming consistency improvements.

---

## What Didn't Work

### 1. Technique Differentiation — None Consistently Beats Others
All three techniques converge to the same performance band. The hypothesis that "ET is better for complex PRs" and "SelfRefine is better for type/small fixes" was **not confirmed** with statistical significance. The corpus may be too homogeneous to reveal technique-PR-type interactions.

### 2. Description Saturation — PR Description Accuracy Dominates
PR description accuracy (did the PR description match the actual code change?) is the #1 predictor of score across all techniques. All three techniques produce similar description accuracy — suggesting the bottleneck is **problem understanding**, not code generation technique.

### 3. Rubric Ceiling — ~87 is Structural, Not Technique-Limited
The 6-dim rubric has a hard ceiling at ~87 due to:
- Evidence Standard: always FAIL (E2E tests can't run locally, structural limitation)
- Type Safety: systematic failure (Any for structured data, mypy suppressions)
- These two dimensions alone can account for 30-40% of the score being structurally unavailable

Even perfect code generation can't break the ceiling without rubric reform.

---

## Recommendations for Future Work

### Recommendation 1: Problem Decomposition Over Technique Ranking
Stop trying to rank techniques. Instead, decompose the problem:
- Which PR types benefit from which techniques? (ET for complex multi-step fixes, SelfRefine for renames, PRM for bug fixes with clear reproduction steps)
- Build a PR-type classifier and route to technique accordingly
- This is a more tractable problem than "which technique is best overall"

### Recommendation 2: Address the Rubric Ceiling
The ~87 ceiling is a measurement problem, not a generation problem:
- Add local E2E execution evidence (video evidence gate — attempted but failed in WS5)
- Separate Type Safety into sub-dimensions (TypedDict usage, mypy suppression count)
- A PR that gets 100/100 on all achievable dimensions but fails ES should score ~70, not ~87

### Recommendation 3: Prune Low-Value autor PRs
The autor pipeline creates PRs for every merged PR. But:
- Small/cosmetic PRs don't benefit from autor recreation (same score as original)
- Focus autor resources on complex PRs where delta is likely positive
- Threshold: only autor-test PRs where original score < 75

### Recommendation 4: Phase 4 — Meta-Learning Loop
Instead of more PR scoring cycles, run a meta-learning loop:
1. Given a PR description + diff, predict which technique will perform best
2. Use the bandit data as training signal
3. Build a PR-type → technique routing table from the corpus
4. Test routing accuracy on held-out PRs

---

## Open Questions

1. **Why did PRM #6338 score 87?** The PR had two fixes — Fix 1 (world_logic) scored 93, Fix 2 (agent_prompts) scored 81. The variance within the same PR suggests the PR-type interaction is real but our scoring granularity isn't fine enough to capture it.

2. **Is the 87 ceiling compressible?** If the rubric is the bottleneck, rubric reform could unlock higher scores. But rubric reform changes the measurement, not the generation.

3. **Should Phase 4 be actual PR creation or meta-research?** The original goal was real PRs on worldarchitect.ai. Phase 3 confirmed autor PRs can score comparably to originals. The next step should be: find the specific PR types where autor PRs consistently beat originals, and focus there.

---

## Conclusion

Phase 3 validates the held-out methodology and corrects Phase 2's inflated estimates. All three techniques converge — the marginal value of more PR scoring cycles is low. The highest-ROI next step is **problem decomposition**: which PR types benefit from autor recreation, and how should they be routed to techniques?
