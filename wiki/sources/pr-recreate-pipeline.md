---
title: "PR Recreate Pipeline"
type: source
tags: [auto-research, pr-recreation, swebench, technique-evaluation]
date: 2026-04-15
source_file: nextsteps/pr-recreate-pipeline.md
---

## Summary

PR Recreate Pipeline pivots from benchmark mode (predicting historical PRs) to actual code production. For each merged PR: sync worktree to pre-merge commit, recreate the fix from scratch using a technique (SelfRefine, PRM, SWE-bench), compare the recreation to the original PR diff, and score against canonical ideal patterns.

## Key Claims

- **Benchmark mode → production mode**: Current system predicts what already-merged PRs would do; new pipeline actually fixes from pre-state and produces real code
- **Key metric: Delta = canonical_score - original_pr_score**: Positive delta means technique improved on the original PR's implementation
- **Recreation accuracy**: % of original PR diff lines correctly predicted; separate over/under-prediction rates
- **SWE-bench style**: Pre-PR commit → agent recreates → compare diffs → score → offer to open real PR

## Key Quotes

> "The current auto-research system is a benchmark — it predicts what already-merged PRs would do, scores prediction accuracy, but produces zero real code changes. This is not valuable." — jleechan, 2026-04-15

## Pipeline Steps

1. **SELECT** PR from worldarchitect.ai (merged, <500 lines, real bug fixes)
2. **FIND PRE-MERGE COMMIT**: `git merge-base HEAD~ PR_number~`
3. **SYNC WORKTREE**: `git worktree add pre-PR-commit`
4. **RECREATE FIX**: Agent applies technique in pre-PR state
5. **COMPARE DIFFS**: recreation_diff vs original_PR_diff (% correct, over/under)
6. **SCORE vs CANONICAL**: 6-dimension rubric (Naming 15%, Error Handling 20%, Type Safety 20%, Architecture 20%, Test Coverage 15%, Documentation 10%)
7. **RECORD**: recreation_accuracy, canonical_score, original_score, delta

## Benchmark vs Recreate Comparison

| Benchmark Mode | Recreate Mode |
|---------------|---------------|
| Predict what already happened | Actually fix from pre-state |
| Zero real code produced | Real code changes (can be PR'd) |
| Measures prediction accuracy | Measures fix quality + prediction |
| Historical PRs only | Any open issue can be targeted |
| Score only | Score + potential real PR |

## Scoring

**Recreation Accuracy**: % of original PR diff lines correctly predicted; over-prediction rate (added lines not needed); under-prediction rate (missed lines)

**Canonical Score**: 6-dimension rubric against ideal patterns from FastAPI, Requests

**Key Metric**: Delta = canonical_score - original_pr_score
- Positive: technique improved on original
- Negative: original was already good enough

## Agent Team Structure

- **selector**: Picks next PR, finds pre-merge commit
- **recreator**: Applies technique in pre-PR worktree
- **comparer**: Diffs recreation vs original, scores canonical
- **recorder**: Logs to research-wiki/syntheses/

## Implementation Phases

1. Phase 1: Build worktree sync + pre-PR commit finder
2. Phase 2: Integrate with SelfRefine technique
3. Phase 3: Compare 5 PRs (recreation + canonical scoring)
4. Phase 4: If delta > 0, offer to open real PR
5. Phase 5: Full automation with parallel agents

## Connections

- [[SelfRefine]] — technique to use in recreation
- [[ProcessRewardModel]] — technique to use in recreation
- [[SWE-bench]] — inspiration for approach
- [[CanonicalCodeScorer]] — scoring rubric
- [[ExtendedThinking]] — technique to use in recreation
