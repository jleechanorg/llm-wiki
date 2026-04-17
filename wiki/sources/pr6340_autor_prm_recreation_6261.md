---
title: "PR #6340 — [autor/PRM] refactor(rewards): migrate to centralized robust numeric extraction"
type: source
tags: [autor, PRM, numeric-extraction, rewards, defensive]
date: 2026-04-17
source_file: ../raw/pr6340_autor_prm_recreation_6261_2026-04-17.md
---

## Summary
PRM autor PR recreating [[PR6261]] using the Process Reward Model (PRM) technique. PRM applies step-by-step reasoning with explicit reward signal evaluation at each step before proceeding. Scored 77/100 using the 6-dimension canonical pattern rubric.

## PRM Technique
PRM differs from [[SelfRefine]] (3-iteration critique loop) and [[ExtendedThinking]] (extended CoT without explicit step evaluation) by:
1. **Explicit step reasoning**: each step is reasoned through before proceeding
2. **Reward signal evaluation**: at each decision point, evaluate whether the choice improves the solution
3. **Traceable reasoning**: the reasoning process is visible in comments explaining WHY each decision was made

## Changes (390 lines diff vs 292 for original)
- `mvp_site/schemas/defensive_numeric_converter.py` — regex-based number extraction from LLM-hallucinated strings like "500 XP", "1,000 gp"; added `OverflowError` handling
- `mvp_site/tests/test_defensive_numeric_central_robustness.py` — new test file
- `mvp_site/world_logic.py` — robust numeric extraction wired into world logic
- `testing_mcp/test_rewards_box_robustness.py` — new test file

## 6-Dimension Rubric Score: 77/100
| Dimension | Score | Max |
|-----------|-------|-----|
| NAMING | 12 | 15 |
| ERROR HANDLING | 16 | 20 |
| TYPE SAFETY | 16 | 20 |
| ARCHITECTURE | 15 | 20 |
| TEST COVERAGE | 10 | 15 |
| DOCUMENTATION | 8 | 10 |

## Key PRM Improvement Over Original
PRM version added `OverflowError` to the exception tuple (original only caught `ValueError, TypeError`), providing more robust error handling for edge cases.

## Connections
- [[PR6261]] — the original merged PR being recreated
- [[AutorPR]] — AI-generated PR using PRM technique
- [[ProcessRewardModel]] — the PRM technique
- [[ThompsonSamplingBandit]] — bandit updated: PRM n=10, mean=81.4
