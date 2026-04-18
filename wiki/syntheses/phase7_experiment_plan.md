---
title: "Phase 7 Experiment Plan: Multi-Exemplar + PR-Type Classification"
type: synthesis
tags: [phase7, experiment-plan, multi-exemplar, pr-type-classification]
sources: [phase6_all_variants_summary]
last_updated: 2026-04-18
---

# Phase 7 Experiment Plan: Multi-Exemplar + PR-Type Classification

## Prior Results

| Technique | Mean | Delta vs Baseline | Status |
|-----------|------|-------------------|--------|
| SR-fewshot (1-exemplar) | 85.75 | +4.52 | Baseline |
| SR-metaharness | 84.04 | +2.81 | Good |
| SR-5iter | 82.36 | +1.13 | Modest |
| SR baseline | 81.23 | — | Baseline |

Phase 7 hypothesis: multi-exemplar guidance (+1 per PR type) and PR-type classification will outperform single-exemplar SR-fewshot.

## PR-Type Taxonomy (3 Types)

| Type | Label | Exemplar PR | Score | Files |
|------|-------|-------------|-------|-------|
| State Semantics | `state-bool` | #6243 | 97.5 | game_state.py |
| Data Normalization | `data-norm` | #6261 | 89 | world_logic.py |
| CI/Workflow | `ci-workflow` | #6269 | 85.3 | skeptic-gate YAML |

## Experiment Matrix

### Phase 7c: SR-multi-exemplar (Task 5)
**Hypothesis:** Showing 1 exemplar per PR type beats showing only the best single exemplar (6243 @ 97.5).

**Prompt variant:** Show all 3 type-exemplars in the prompt. Let the model select which pattern to follow based on PR context.

**Runs:** 4 PRs × 3 runs = 12 runs. PRs: 6265, 6261, 6245, 6269.

### Phase 7d: SR-prtype (Task 4)
**Hypothesis:** Classifying PR type before generation and selecting the type-specific exemplar outperforms both single-exemplar and multi-exemplar (no-classification).

**Prompt variant:** First classify the PR into one of the 3 types, then show ONLY the type-specific exemplar.

**Runs:** Same 4 PRs × 3 runs = 12 runs.

### Comparison Baseline: SR-fewshot (from Phase 6)
- PRs 6265, 6261, 6245, 6269: means 87.9, 84.58, 87.37, 84.4 = avg 86.06
- This is the Phase 6 SR-fewshot on the same 4 PRs (excluding 6243 which was the exemplar itself)

## Metrics

- Mean score per technique
- Delta vs SR-fewshot baseline (86.06 on these 4 PRs)
- Per-dimension breakdown (naming, error_handling, type_safety, architecture, test_coverage, documentation)
- Per-PR type performance

## Scoring Protocol

Same rubric as Phase 6 (6 dimensions, 100-point scale, MiniMax-M2 scoring).

## Run Session IDs

- Phase 7c: `phase7-multi-exemplar-YYYYMMDD`
- Phase 7d: `phase7-prtype-YYYYMMDD`

## Artifacts

- Score JSONs: `research-wiki/scores/SR-multi-exemplar_*.json`
- Score JSONs: `research-wiki/scores/SR-prtype_*.json`
- Logs: `wiki/syntheses/et_logs/SR-multi-exemplar_*.log`
- Logs: `wiki/syntheses/et_logs/SR-prtype_*.log`
- Synthesis: `wiki/syntheses/phase7_results.md`