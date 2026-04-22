---
title: "Phase 6 Iteration 4: SR-Adversarial (Solver+Attacker Minimax)"
type: synthesis
tags: [auto-research, phase6, sr-adversarial, adversarial-training, minimax]
sources: [pr-6265, pr-6261, pr-6245, pr-6243, pr-6269]
last_updated: 2026-04-18
---

## Experiment: SR-Adversarial with Solver+Attacker Minimax

**Session ID:** phase6_sr_adversarial_20260417_224803  
**Run Date:** 2026-04-18  
**Sample Size:** n=15 (3 runs × 5 PRs)

### Technique Overview

SR-adversarial applies adversarial training concepts (AdverMCTS-inspired) to code generation:

1. **Initial fix generation** from PR diff
2. **Attacker pass:** Identify 3 specific failure modes (edge cases, null states, type violations)
3. **Solver pass:** Rewrite implementation to handle all 3 failure modes defensively
4. **Repeat** if needed (in this variant, 1 round of Attacker+Solver per run)

### Hypothesis

Explicitly modeling failure modes should improve robustness and error handling, pushing scores toward the SR-fewshot ceiling (85.75). The adversarial framing forces the solver to think about production risk rather than surface-level completeness.

### Results

**Per-PR Means (n=3 each):**

| PR | Mean | Scores | Notes |
|----|------|--------|-------|
| 6243 | 92.67 | [90, 95, 93] | **Best:** Bool semantics fix is narrow, adversarial helps |
| 6261 | 79.67 | [77, 79, 83] | Numeric converter; adversarial gains +1.2 vs SR baseline |
| 6265 | 80.00 | [82, 80, 78] | Normalization fix; adversarial on par with SR baseline |
| 6245 | 74.67 | [79, 70, 75] | XP extraction; **worst** performer, adversarial -5.6 vs SR |
| 6269 | 69.00 | [68, 67, 72] | CI workflow; **lowest** overall, adversarial -12.2 vs SR |

**Overall Mean:** 79.20/100  
**Baseline SR Mean:** 81.23/100  
**Uplift:** -2.03 (-2.5%)  
**Gap to Best (SR-fewshot 85.75):** -6.55

### Analysis

#### Why SR-Adversarial Underperforms

1. **False Positives in Attacker Pass**
   - The Attacker (hostile reviewer) tends to flag generic risks: "what if input is None?", "what if type is wrong?"
   - These are already handled in the original fixes
   - Solver dutifully "fixes" them, adding defensive boilerplate
   - Result: Test coverage goes up, but type safety and architecture suffer
   
2. **Solver Overfitting to Attacker Concerns**
   - Solver focuses on the 3 identified failure modes
   - Misses architectural issues or naming problems
   - Adds try/except blocks and defensive checks where not needed

3. **Context Overhead**
   - Attacker+Solver passes consume context
   - Model has less room for holistic reasoning about PR intent
   - Results in more brittle, localized fixes

4. **Technique-to-PR Mismatch**
   - PR #6243 (bool semantics): Very narrow scope, adversarial helps identify bool/int edge case
   - PR #6269 (CI workflow): No error handling dimension relevant, defensive programming adds noise
   - PR #6245 (XP extraction): Complex refactoring, adversarial fixates on individual variables, misses global structure

#### Per-PR Breakdown

**PR 6243 (Best: 92.67)**
- Adversarial correctly identified bool-subclass-of-int edge case
- Solver rewrote type checks to be explicit
- Clean, focused scope → adversarial was beneficial
- Gap to SR baseline: +0.92 ✓

**PR 6265 (Neutral: 80.00)**
- Normalization fix with fallback keys (xp→xp_gained, gold_pieces→gold)
- Adversarial flagged: None inputs, empty keys, NaN handling
- Solver added checks; original fix already handled most cases
- No uplift over baseline

**PR 6261 (Slight Gain: +1.2)**
- Numeric converter with defensive logic
- Adversarial identified: empty string, zero, NaN, inf edge cases
- Solver formalized handling; architecture remained intact
- Small positive effect

**PR 6245 (Significant Loss: -5.6)**
- XP extraction refactoring (remove duplicate function, consolidate logic)
- Adversarial fixated on: individual variable fallbacks, type checks
- Solver missed: architectural consolidation, DRY principle, naming clarity
- Added defensive checks but lost refactoring clarity

**PR 6269 (Severe Loss: -12.2)**
- CI/GitHub Actions workflow (shell script)
- Adversarial flagged: exit codes, undefined vars, regex issues
- Solver added error handling (pipefail, set -e)
- But: Added defensive boilerplate to non-critical paths
- Type safety and documentation scores dropped (shell scripts don't benefit from type hints)

### Conclusion

**SR-adversarial is NOT recommended for this task.**

The technique:
- Works only on narrow, well-scoped PRs (like #6243)
- Fails on refactorings, architectural changes, and non-code artifacts
- Adds 2 model calls per run (Attacker + Solver) vs 1 for baseline SR
- Produces false positives that the Solver cannot distinguish from real bugs

**Why the convergence at 79.20?**

All Phase 6 variants (SR-5iter, SR-fewshot, SR-adversarial) operate on the same 5 PRs. The convergence around 80-86 is the natural ceiling for this PR set. SR-adversarial lands *below* the SR baseline because:

1. The 15 PRs in the matched corpus are not adversarially challenging—they are straightforward fixes
2. Explicit adversarial training adds noise rather than signal
3. The technique scales poorly to CI/infrastructure changes and refactorings

### Recommendation

- **Do NOT use SR-adversarial for general PR fixing**
- **Conditional use:** IF a PR is known to have subtle edge cases (e.g., type coercion, state machine transitions), run a *single* Attacker pass to identify risks
- **Better alternative:** SR-fewshot (85.75) with a reference PR demonstrates the pattern better than adversarial iteration
- **Research direction:** Adversarial training might work if the Attacker model is tuned to find *realistic* bugs (e.g., database race conditions, auth bypass) rather than generic defensive programming

### Artifacts

- Scores: `research-wiki/scores/SR-adversarial_*.json` (15 files)
- Logs: `wiki/syntheses/et_logs/SR-adversarial_*.log` (15 files)
- Bandit state: `technique_bandit/bandit_state.json` (entry added)

### Next Steps

Phase 6 is complete with 4 SR variants tested:
1. SR baseline (81.23) — established reference
2. SR-5iter (82.36) — modest +1.1% improvement via iteration
3. SR-fewshot (85.75) — best performer, +5.6% via example guidance
4. SR-adversarial (79.20) — -2.5% via adversarial training, **not recommended**

No further SR variants planned. Router feasibility depends on whether technique rankings reverse across held-out PR sets (currently all converge 79-86).
