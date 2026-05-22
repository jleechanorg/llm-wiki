---
title: "autor SR-5iter Technique"
type: concept
tags: [autor, self-refine, sr-5iter, technique, 5-iteration]
sources: [autor-sr-adversarial-design-2026-05-13]
last_updated: 2026-05-13
---

# autor SR-5iter Technique

## Overview

SR-5iter is a 5-round self-refinement technique. It replaces the standard 3-round SR with more thorough iteration cycles.

## Iteration Rounds

| Round | Focus |
|---|---|
| 1 | Review fix against code quality standards, identify 2-3 specific improvements |
| 2 | Apply improvements, check for new issues |
| 3 | Refine error handling and type safety, verify edge cases |
| 4 | Check architecture and naming, ensure module boundaries are clean |
| 5 | Final polish — documentation, comments, and any last improvements |

## Implementation

`scripts/batch_sr5iter.py` runs the SR-5iter batch. The system prompt:

> "You are an expert code reviewer and fixer. Generate production-ready code fixes for GitHub PRs with 5 rounds of self-refinement."

The generation prompt instructs the model to perform all 5 rounds and output final code with brief refinement notes.

## Batch targeting

The batch targets PRs that have only 1 run, adding runs to reach 3 each:
- Target PRs: 6409, 6418, 6420, 6429, 6432, 6434, 6436, 6437, 6438, 6443, 6444
- For 15-run batch: 5 PRs × 3 runs = 15 total

PRs already at n=3 (6243, 6245, 6261, 6265, 6269) are skipped.

## Note

SR-5iter is not in the `--technique` choices for `run_autor_experiment.py`. It exists only in `batch_sr5iter.py` as a separate batch runner. SR-adversarial is the new technique in run_autor_experiment.py.

## See also

- [[autor-router-prerequisite-gate]]
- [[autor-sr-adversarial-design-2026-05-13]]
- [[validate_router_prereqs.py]]