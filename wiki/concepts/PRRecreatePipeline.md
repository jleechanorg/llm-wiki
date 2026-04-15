---
title: "PR Recreate Pipeline"
type: concept
tags: [pr-recreation, auto-research, swebench, technique-evaluation, production-mode]
sources: [pr-recreate-pipeline]
last_updated: 2026-04-15
---

## Summary

PR Recreate Pipeline shifts auto-research from **benchmark mode** (predict what already-merged PRs would do) to **production mode** (actually fix from pre-PR state, compare, and potentially open real PRs).

## How It Works

1. Pick a merged PR in worldarchitect.ai
2. Find the pre-merge commit (`git merge-base`)
3. Sync worktree to pre-merge state
4. Agent recreates the fix using a technique (SelfRefine, PRM, SWE-bench, ExtendedThinking)
5. Compare recreation diff vs original PR diff
6. Score recreation against canonical ideal (FastAPI, Requests patterns)
7. If delta > 0 (technique beats original), offer to open real PR

## Key Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Recreation Accuracy** | % of original diff lines correctly predicted |
| **Over-prediction** | Lines added that weren't in original |
| **Under-prediction** | Lines from original that were missed |
| **Canonical Score** | 6-dim rubric vs ideal patterns (same as before) |
| **Delta** | canonical_score - original_pr_score |

## Delta Interpretation

| Delta | Meaning |
|-------|---------|
| Positive | Technique improved on the original PR |
| Zero | Technique matched original |
| Negative | Original was already good enough |

## Why This Beats Benchmark Mode

Benchmark mode measures prediction accuracy but produces zero real code. Recreate mode:
- Actually fixes from pre-state (real code)
- Can open real PRs if delta > 0
- Tests whether techniques can do better than originals
- Works on open issues (not just historical PRs)

## Agent Team

- [[AgentTeam-PrRecreate]] — selector, recreator, comparer, recorder roles
- [[SelfRefine]] — technique for recreate step
- [[ProcessRewardModel]] — technique for recreate step
- [[SWE-bench]] — inspiration for approach
- [[CanonicalCodeScorer]] — scoring rubric

## Status

Proposed 2026-04-15. Awaiting implementation of Phase 1.
