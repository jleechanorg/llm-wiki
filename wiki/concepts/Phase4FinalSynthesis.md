---
title: "Phase4FinalSynthesis"
type: concept
tags: [phase4, final-synthesis, bandit, autor, technique-ranking]
date: 2026-04-16
---

## Definition
Phase 4 final synthesis of the auto-research experiment. Confirms all three code generation techniques (SelfRefine, ET, PRM) converge to the same performance band (~80-87) with overlapping confidence intervals. The ~87 ceiling is a **rubric artifact**, not a technique ceiling.

## Final Bandit State (Post Phase 3)

| Technique | Mean | n | α | β |
|-----------|------|---|---|---|
| SelfRefine | 83.8 | 26 | 20.3 | 9.8 |
| ET | 82.5 | 12 | 10.4 | 5.6 |
| PRM | 82.0 | 8 | 7.7 | 4.3 |

**Interpretation**: All three techniques converge — no statistically significant winner. SelfRefine has most data (n=26). ET and PRM have wider CIs.

## Key Findings

### Held-Out Validation Corrected Phase 2 Bias
- Phase 2 SelfRefine estimate: **87.5** (biased — non-held-out methodology)
- Phase 3 held-out estimate: **80.2** (corrected — 7.3 point correction)

### PRM Advantages Appear on Complex PRs
PRM #6338 scored 87/100 (highest in Phase 3). The PR had two fixes — Fix 1 (world_logic) scored 93, Fix 2 (agent_prompts) scored 81. The within-PR variance suggests **PRM advantages are real but our scoring granularity isn't fine enough**.

### Rubric Ceiling at ~87 is Structural
Two dimensions are structurally unavailable regardless of technique:
- **Evidence Standard**: always FAIL (E2E tests can't run locally)
- **Type Safety**: systematic AnyTypedDict gaps, mypy suppressions
- These account for 30-40% of score being structurally unavailable

### Problem Decomposition > Technique Ranking
Stop ranking techniques. Instead:
1. Which PR types benefit from which techniques?
2. ET for complex multi-step fixes
3. SelfRefine for renames and consistency improvements
4. PRM for bug fixes with clear reproduction steps
5. Build a PR-type classifier and route accordingly

## Recommendations

1. **Problem decomposition**: Build PR-type → technique routing table from corpus
2. **Rubric reform**: Separate Type Safety into sub-dimensions; add local E2E execution evidence
3. **Prune low-value autor PRs**: Only autor-test PRs where original score < 75
4. **Phase 4 meta-learning**: Given PR description + diff, predict which technique will perform best

## Connections
- [[ThompsonSamplingBandit]] — bandit that tracked technique posterior
- [[AutorPR]] — AI-generated PRs evaluated in Phase 3/4
- [[SelfRefine]], [[ExtendedThinking]], [[ProcessRewardModel]] — techniques studied
- [[Phase3HeldOutValidation]] — held-out methodology that corrected Phase 2 bias
