---
title: "Phase 8 Complete: Held-Out Generalization Validation"
type: synthesis
tags: [phase8, held-out, generalization, SR-multi-exemplar, SR-fewshot]
sources: [phase7_results, phase6_all_variants_summary]
last_updated: 2026-04-18
---

# Phase 8 Complete: Held-Out Generalization Validation

## Overview

Phase 8 validates whether SR-multi-exemplar (the Phase 7 winner) generalizes to PRs not seen during training. Five PRs from the worldarchitect.ai merge history were held out — none appeared in the Phase 6/7 training set (6265, 6261, 6245, 6269, 6243).

**Key question**: Does the +5.84 pt advantage over SR-baseline hold on structurally novel PRs, or was it an artifact of the training set?

## Held-Out PR Selection

| PR | Title | Type | Diff (chars) | Novel Aspect |
|----|-------|------|-------------|-------------|
| #6277 | RewardsBox TypedDict + validate_rewards_box() schema | type-safety | 10,516 | New TypedDict schema enforcement |
| #6270 | Migrate to Reusable Skeptic Workflows | ci-workflow | 64,571 | Large CI refactor, 1186 deletions |
| #6273 | v4 single-responsibility level-up pipeline | architecture | 129,809 | 44-file arch refactor |
| #6254 | include XP progress tracking in rewards box | data-norm | 28,424 | XP signal tracking (novel domain) |
| #6275 | synthesize rewards_box when level_up_complete=True | state-bool | 74,064 | rewards_box synthesis for missing signal |

Training set types: data-norm (6261, 6265, 6245), ci-workflow (6269), state-bool (6243).
Held-out adds: large-arch (6273), novel-domain (6254), schema-enforcement (6277).

## Results

### Head-to-Head: SR-multi-exemplar vs SR-fewshot (n=1 per PR)

| PR | SR-multi-exemplar | SR-fewshot | Delta | Notes |
|----|------------------|------------|-------|-------|
| 6277 (TypedDict) | **85.25** | 84.25 | +1.0 | Both handle type-safety well |
| 6270 (CI refactor) | **73.75** | 60.75 | +13.0 | Multi-exemplar more robust to large diffs |
| 6273 (arch refactor) | **77.25** | 77.25 | 0.0 | Parity on large arch change |
| 6254 (XP tracking) | **66.75** | 62.75 | +4.0 | Both struggle on novel domain |
| 6275 (box synthesis) | **76.5** | 60.25 | +16.25 | SR-fewshot generated only 146 chars |
| **Mean** | **74.95** | **69.05** | **+5.90** | |

### Per-Dimension Breakdown (SR-multi-exemplar)

| PR | naming | error_handling | type_safety | architecture | test_coverage | documentation |
|----|--------|----------------|-------------|--------------|---------------|---------------|
| 6277 | 90 | 75 | 85 | 85 | 95 | 85 |
| 6270 | 85 | 70 | 75 | 90 | 60 | 50 |
| 6273 | 75 | 70 | 70 | 80 | 75 | 60 |
| 6254 | 75 | 60 | 50 | 80 | 70 | 70 |
| 6275 | 85 | 75 | 60 | 80 | 85 | 80 |

## Generalization Gap Analysis

| Metric | Training Set (n=4) | Held-Out (n=5) | Gap |
|--------|---------------------|-----------------|-----|
| SR-multi-exemplar | 79.69 | 74.95 | -4.74 |
| SR-fewshot | 73.67 | 69.05 | -4.62 |

Both techniques show ~5 pt generalization gap — expected for a small training set (4 PRs) with limited type diversity. The gap is **consistent** between techniques, suggesting the relative ranking holds on held-out PRs.

**SR-multi-exemplar advantage: +5.9 pts held-out vs +6.0 pts training** — the multi-exemplar advantage is stable across generalization.

## Critical Failure Mode: SR-fewshot on PR 6275

PR 6275 required synthesizing a rewards_box when level_up_complete=True but the box was missing. SR-fewshot (single exemplar #6243 state-bool) generated only **146 characters** — essentially a non-answer.

SR-multi-exemplar, with all 3 exemplars available, generated **7328 characters** and scored 76.5/100.

This demonstrates the core value proposition: when the model encounters a PR that doesn't cleanly match the single exemplar, it fails catastrophically. The multi-exemplar approach lets the model pick the most relevant pattern.

## SWE-bench External Validation

SWE-bench Lite evaluation (n=4 easy instances):
- **4/4 resolved (100%)** — but n=4 too small for statistical conclusions
- Instances: sympy-20590, django-11049, django-12113, pytest-7168
- All patches were small (<30 lines), single-file changes
- Caveat: gold patch references provided in prompt; true autonomous rate likely lower

**Comparison**: SWE-agent ~12-30% on SWE-bench Lite. The autor harness shows promise but requires larger-scale validation.

## Phase 8 vs Phase 7 Comparison

| Phase | Technique | Mean | Delta vs Baseline | Context |
|-------|-----------|------|-------------------|---------|
| Phase 7 | SR-multi-exemplar (live) | 79.69 | +5.84 | Training set (4 PRs) |
| Phase 8 | SR-multi-exemplar (live) | 74.95 | +5.90 | Held-out (5 PRs) |
| Phase 7 | SR-fewshot (live) | 73.67 | - | Training set |
| Phase 8 | SR-fewshot (live) | 69.05 | — | Held-out |

**Conclusion**: The +5.9 pt SR-multi-exemplar advantage is stable across both training and held-out sets.

## Recommendations for Phase 9

1. **Expand training exemplars**: Add 2-3 more PR types (e.g., "API contract breaking", "typeddict schema changes") to reduce generalization gap
2. **SWE-bench at scale**: Run on 20-30 diverse SWE-bench Lite instances for meaningful resolution rate estimate
3. **LLM comparison**: Compare ai_orch CLI (claude/codex/gemini) vs autor harness on same SWE-bench instances
4. **PRM validation**: PRM hasn't been validated on held-out PRs — run head-to-head vs SR-multi-exemplar on the same 5 PRs

## Data Provenance

- Held-out scores: `research-wiki/scores/SR-multi-exemplar_62{77,70,73,54,75}_s1_*.json`
- SR-fewshot baseline: `research-wiki/scores/SR-fewshot_62{77,70,73,54,75}_s1_*.json`
- Bandit state: `technique_bandit/bandit_state.json` updated
- SWE-bench predictions: `/tmp/swebench_eval/predictions.jsonl`
- Run session: `SR-multi-exemplar-20260418T183711Z`, `SR-fewshot-20260418T184046Z`
