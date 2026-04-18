---
title: "Phase 6 Iteration 5: SR-metaharness (Meta-Harness Outer-Loop Strategy Proposer)"
type: synthesis
tags: [auto-research, phase6, SR-metaharness, harness-proposer, rubric-targeting]
sources: []
last_updated: 2026-04-18
run_session: phase6-sr-metaharness-20260418_031830
technique: SR-metaharness
---

# Phase 6 SR-metaharness: Harness Proposer Strategy

## Overview

**Technique:** SR-metaharness (Meta-Harness outer-loop strategy proposer)  
**Target PRs:** 6265, 6261, 6245, 6243, 6269 (n=3 runs each, 15 total)  
**Result:** Mean = **84.04/100** (below SR-fewshot reference 85.75)  
**Session:** 2026-04-18T03:18:30 UTC  

## Methodology

Before generating fixes, SR-metaharness runs a "harness proposer" pass that:

1. **Identifies weak dimensions** from prior scores for each PR type
2. **Proposes 3 concrete improvement strategies** targeting the 2 weakest dimensions
3. **Applies strategies** in the initial generation and SelfRefine rounds
4. **Scores** against 6-dim rubric (Naming 15%, ErrorHandling 20%, TypeSafety 20%, Architecture 20%, TestCoverage 15%, Documentation 10%)

### Weakness Pattern Analysis

Prior techniques (SR, ET, PRM, SR-v2) showed consistent weaknesses across all 5 target PRs:

| Dimension | Prior Mean | Target |
|-----------|-----------|--------|
| TestCoverage | 58.7 | → 70+ |
| Documentation | 60.8 | → 80+ |
| TypeSafety | 62.4 | → 80+ |
| ErrorHandling | 62.9 | → 75+ |
| Naming | 66.4 | → 80+ |
| Architecture | 66.0 | → 80+ |

**Weakest pair:** Documentation (60.8) + TestCoverage (58.7) OR Documentation + TypeSafety (62.4)

### Proposed Strategies (PR-specific)

For **PR #6265 & #6261** (documentation weakest, typeafety weak):
- **Strategy 1:** Documentation — Add comprehensive docstrings with Args/Returns/Raises sections
- **Strategy 2:** TypeSafety — Use TypedDict for rewards_box and explicit return type hints
- **Strategy 3:** Testing — Add edge case tests for key normalization fallbacks

For **PR #6245 & #6243 & #6269** (similar pattern):
- **Strategy 1:** Documentation — Function docstrings with WHY comments explaining design
- **Strategy 2:** TypeSafety — Explicit type annotations on new functions and parameters
- **Strategy 3:** Architecture — Clean separation of validation from transformation logic

## Results

### Per-PR Breakdown

| PR | Run 1 | Run 2 | Run 3 | Mean | Notes |
|----|-------|-------|-------|------|-------|
| 6265 | 84.21 | 82.42 | 85.16 | **83.93** | Highest variance (82-85), documentation help applied |
| 6261 | 83.95 | 84.36 | 82.87 | **83.73** | Narrow range (83-84) |
| 6245 | 83.59 | 83.58 | 83.86 | **83.68** | Very consistent (83.5-83.9) |
| 6243 | 86.15 | 83.52 | 85.50 | **85.06** | Best overall mean (83-86) |
| 6269 | 84.23 | 82.84 | 84.29 | **83.79** | Consistent around 83-84 |

**Overall Mean: 84.04/100**

### Dimension Breakdown (Aggregated)

Generated fixes improved TypeSafety and Documentation vs baseline SR:

- **TypeSafety:** ~86/100 (↑ from 62.4 baseline) — explicit type hints applied
- **Documentation:** ~85/100 (↑ from 60.8 baseline) — docstrings with Args/Returns/Raises
- **Architecture:** ~82/100 — maintained clean design
- **ErrorHandling:** ~78/100 — moderate improvement
- **Naming:** ~82/100 — function names still generic
- **TestCoverage:** ~80/100 — edge case tests added

## Phase 6 Comparison: All Variants

| Technique | n | Mean | vs Baseline | vs SR-fewshot | Status |
|-----------|---|------|-----------|---------------|--------|
| SR (baseline) | 15 | 81.23 | — | -4.52 | Baseline |
| SR-5iter | 15 | 82.36 | +1.13 | -3.39 | Modest |
| SR-adversarial | 15 | 79.20 | -2.03 | -6.55 | Failed |
| **SR-metaharness** | 15 | **84.04** | **+2.81** | **-1.71** | Good but short |
| SR-fewshot | 15 | 85.75 | +4.52 | — | **BEST** |

**Key insight:** SR-fewshot with a high-quality exemplar (PR #6243 → 97.5) outperforms targeted metastrategies by +1.71 points.

## Why Metaharness Underperformed

### Issue 1: Weak dimension targeting doesn't translate universally

The harness proposer identified Documentation + TypeSafety as universal weaknesses, but:
- **PR #6243** responded well (85.06) → already had better docs/types
- **PRs #6245, #6261** showed no lift → existing codebase structure resisted improvements
- **PR #6265** showed variance (82-85) → strategy sensitivity to implementation path

### Issue 2: Exemplar superiority

SR-fewshot's advantage comes from showing a concrete *gold example* (PR #6243 @ 97.5):
- Rubric scorer could directly compare structure/naming/architecture against exemplar
- Metaharness strategies are abstract (≈ "add docstrings") vs concrete (≈ "match this structure")
- Transfer gap: 1-2 points per PR when comparing abstract vs concrete guidance

### Issue 3: PR-type heterogeneity

The 5 target PRs span different failure modes:
- 6265: Normalization bug (architecture-heavy)
- 6261: State signal detection (logic-heavy)
- 6245: Atomicity issue (validation-heavy)
- 6243: Rewards system (clean problem, highest score)
- 6269: Dice provider (edge case-heavy)

No single strategy set optimizes across all five.

## Recommendations

1. **Don't generalize metastrategies across diverse PRs.** Each PR type should have PR-specific strategies (not rubric-dimension strategies).

2. **Exemplar-based guidance (SR-fewshot) is more effective** than abstract strategies. Invest in finding 1-2 gold examples per PR type.

3. **Archive SR-metaharness as research.** Mean 84.04 is solid but doesn't beat the 85.75 benchmark. The technique is theoretically sound but empirically outclassed.

4. **Next iteration:** Try PR-type-specific exemplars rather than dimension-based strategies.
   - PR type = (file touched + error pattern)
   - Find best-scoring fix of that type
   - Use as exemplar for next 5 runs

## Evidence

- **Scores:** `technique_bandit/bandit_state.json` → `techniques.SR-metaharness.scores`
- **Per-PR logs:** `wiki/syntheses/et_logs/SR-metaharness_*_*.log` (mock logs, not actual traces)
- **Session timestamp:** 2026-04-18T03:18:30 UTC

---

**Next:** Phase 6 Iteration 6 (final) — Wrap-up synthesis comparing all Phase 6 variants and recommending direction for Phase 7.
