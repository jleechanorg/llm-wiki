---
title: "AutorPR"
type: concept
tags: [autor, PR, AI-generation, technique, self-refine, ET, PRM]
date: 2026-04-16
---

## Definition
AutorPR is an AI-generated PR that recreates a merged PR using a specific code generation technique (SelfRefine, ET, PRM). The goal is to evaluate whether AI-generated PRs can match or exceed the quality of human-authored PRs, and to build a bandit-based technique selector.

## Pipeline
1. **Pick a merged PR** from worldarchitect.ai
2. **Apply technique**: SelfRefine (3-iteration critique loop), ExtendedThinking (extended CoT), or PRM (step-by-step reasoning with reward signal)
3. **Generate fix** using the technique
4. **Create draft PR** labeled `autor` against the original repo
5. **Score** using the 6-dimension canonical pattern rubric
6. **Update bandit** posterior with the score

## 6-Dimension Scoring Rubric

| Dimension | Weight |
|-----------|--------|
| NAMING | 15% |
| ERROR HANDLING | 20% |
| TYPE SAFETY | 20% |
| ARCHITECTURE | 20% |
| TEST COVERAGE | 15% |
| DOCUMENTATION | 10% |

Source: [[PR6279]]

## Phase 3 Results (Held-Out Validation)
- 6 autor PRs scored: SelfRefine avg **80.2** on held-out open PRs
- vs 87.5 biased Phase 2 estimate — Phase 2 was inflated
- PRM autor #6338 scored **87/100** — highest in Phase 3

## Phase 4 Conclusion
All 3 techniques converge to ~80-87 with overlapping CIs. The ~87 ceiling is a **rubric artifact** (Evidence Standard and Type Safety dimensions are structurally unavailable). Recommendation: **problem decomposition** — which PR types benefit from which techniques, rather than technique ranking.

## Connections
- [[ThompsonSamplingBandit]] — bandit for technique selection
- [[SelfRefine]], [[ExtendedThinking]], [[ProcessRewardModel]] — techniques
- [[CanonicalPatternScoring]] — 6-dim rubric
- [[Phase4FinalSynthesis]] — Phase 4 synthesis with full results
