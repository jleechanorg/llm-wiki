# Source: Duplicate PR superset-merge pattern (dark-factory PR #40/#41)

- **Raw**: `raw/feedback_2026-06-09_duplicate_pr_superset_merge.md`
- **Date**: 2026-06-09
- **Type**: learning / feedback
- **Repo**: jleechanorg/dark-factory

## Summary

An Antigravity worker's uncommitted edits were recovered into
[PR #40](https://github.com/jleechanorg/dark-factory/pull/40); the worker later
opened [PR #41](https://github.com/jleechanorg/dark-factory/pull/41) from its
own copy of the same edits — a duplicate work stream (3 of 4 files a strict,
byte-identical subset).

Resolution pattern:

1. Diff the branches directly (`git diff brA brB --stat`) to prove subset vs
   divergence before deciding.
2. Merge the green superset first (#40 → `bf694ad`).
3. `git merge origin/main` into the duplicate's branch: byte-identical hunks
   fall away conflict-free, deflating the PR diff to its unique contribution
   (verified via `gh pr view 41 --json files`).
4. Fix the unique remnant per review, then merge (#41 → `fee8f01`).

Avoids force-push approval, preserves the worker's authorship, and skips rebase
conflict churn. Divergent (non-identical) overlap is instead the
stacked-PR single-writer stop-the-line case.

Ownership handoff corollary: once the superset merges, the duplicate PR becomes
the legitimate owner of follow-up cleanups to formerly-shared files.

## Concepts

- [[Competing-PR-Canonical-Field-Resolution]] — this is the third variant
  (byte-identical duplicate → superset-merge + deflate), alongside
  canonical-field THEIRS-resolution and close-the-subset subsumption.
- [[agent-pr-sprawl]]

Does not affect [[jeffrey-oracle]] — technical workflow learning.
