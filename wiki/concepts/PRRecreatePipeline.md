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

## Critical Harness: Pre-Merge Commit for Merged PRs

**CRITICAL BUG (2026-04-15):** For merged PRs, `git merge-base origin/main refs/pull/<N>/head` returns the **post-merge** commit, NOT the pre-merge state. This caused all 5 parallel recreators to fail (recreating already-merged code).

**Correct approach for merged PRs:**

```bash
# WRONG (returns post-merge for already-merged PRs):
git merge-base origin/main refs/pull/6270/head  # → be963b9c1 (WRONG)

# CORRECT: Use first parent of the merge commit
git log --ancestry-path refs/pull/6270/head..origin/main --first-parent --format=%H | head -1
# → 04d8df0b7 (the merge commit)
git reset --hard 04d8df0b7^1  # → true pre-merge state

# ALTERNATIVE (simpler):
# Find the merge commit on main, then use its first parent
git log --oneline origin/main --ancestry-path refs/pull/<N>/head..origin/main | tail -1
```

**Rule:** Always verify the worktree is at a commit that predates the PR. Check: `git log --oneline -1 HEAD` should NOT include the PR number in its message.

## Agent Team

- [[AgentTeam-PrRecreate]] — selector, recreator, comparer, recorder roles
- [[SelfRefine]] — technique for recreate step
- [[ProcessRewardModel]] — technique for recreate step
- [[SWE-bench]] — inspiration for approach
- [[CanonicalCodeScorer]] — scoring rubric

## Status

Phase 1 attempted 2026-04-15 — failed due to harness bug (merged PR pre-merge detection).
Harness fix documented above. Phase 1 retry pending.
