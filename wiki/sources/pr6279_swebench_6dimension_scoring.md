---
title: "PR #6279 — SWE-bench 6-Dimension Scoring for PRs 6275, 6276, 6277"
type: source
tags: [autor, scoring, swebench, rubric, canonical-patterns]
date: 2026-04-15
source_file: ../raw/pr6279_swebench_6dim_scoring_2026-04-15.md
---

## Summary
PR #6279 introduces SWE-bench-inspired 6-dimension canonical pattern scoring scripts that evaluate PRs against ideal patterns from reference repos (FastAPI, Requests). Scored 3 recent PRs using MiniMax model with weighted rubric. This became the standard scoring methodology for [[AutorPR]] evaluation in [[Phase3AutoResearch]] and [[Phase4FinalSynthesis]].

## 6-Dimension Rubric

| Dimension | Weight | Source |
|----------|--------|--------|
| NAMING | 15% | FastAPI, Requests conventions |
| ERROR HANDLING | 20% | FastAPI typed exceptions |
| TYPE SAFETY | 20% | TypedDict for data shapes |
| ARCHITECTURE | 20% | Canonical repo patterns |
| TEST COVERAGE | 15% | Test quality vs complexity |
| DOCUMENTATION | 10% | Docstrings, comments |

## PRs Scored

### PR #6275 (fix stuck-level-up) — 76/76 tests pass
Synthesizes rewards_box when level_up_complete flag is set. Score: 76/100.

### PR #6276 (feat: Layer 3 CLEAN) — 62/62 tests pass  
Strip old rewards_box field and refactor to single-responsibility level-up pipeline. Score: 62/100.

### PR #6277 (RewardsBox TypedDict) — 10/10 tests pass
Type definition + validate_rewards_box() function. Score: 92.5/100.

## Key Insight
PR description accuracy (did the PR description match the actual code change?) is the #1 predictor of score across all techniques. [[PR6277]] scored highest (92.5) because its description accurately captured a clean, focused change.

## Connections
- [[CanonicalPatternScoring]] — 6-dim rubric against ideal patterns
- [[AutorPR]] — AI-generated PRs scored with this rubric
- [[ThompsonSamplingBandit]] — bandit uses these scores to update technique posterior
- [[Phase3AutoResearch]] — Phase 3 used this scoring for held-out validation
- [[Phase4FinalSynthesis]] — Phase 4 confirmed rubric ceiling at ~87
- [[PR6275]], [[PR6276]], [[PR6277]] — PRs scored by this system
