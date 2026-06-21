---
title: "PR Mid-Review Merge Ancestry Check"
type: concept
tags: [git, pr-workflow, merge-base, orphan-commit, single-writer]
sources: [pr7720-ios-webkit-indexeddb-persistence-deadlock]
last_updated: 2026-06-20
---

# PR Mid-Review Merge Ancestry Check

## Problem

When a `main`-merge (e.g. GitHub "Update branch") is pushed onto a PR branch mid-review, the merge commit is based on the pre-fix HEAD that GitHub had on file at the time. If the PR branch received a later nit-fix commit between the merge-base computation and the push, the new commit is NOT an ancestor of the new head — GitHub's merge silently ORPHANS the nit-fix.

## Observable symptom

A specific line of code (e.g. `configurable: false`) that was on the PR head before the merge disappears after the merge. The CI may pass because the orphaned commit's tests still ran, but the production behavior is reverted.

## Recovery

1. Identify the orphaned SHA from the reflog or `git log --all --oneline | grep <branch>`.
2. `git reset --hard origin/<branch>` to the real head (post-merge).
3. `git cherry-pick <orphaned-sha>` to reapply the dropped fix.
4. Push.

## Prevention rules

- **Single-writer per branch** while driving to green. Do not let GitHub auto-merge `main` into the PR branch while local review fixes are being made.
- After any external push (GitHub merge button, another agent's push), run:
  ```bash
  git merge-base --is-ancestor <local-nitsha> origin/<branch> || echo "ORPHANED"
  ```
  If it prints `ORPHANED`, the local nit is no longer on the head — cherry-pick recovery is needed.
- Prefer **rebase** over merge for updating a PR branch, locally:
  ```bash
  git fetch origin main
  git rebase origin/main
  ```
  This keeps the local commits as ancestors of the new head.

## Related

- [IntegrateHardStopPattern](IntegrateHardStopPattern.md)
- [GreenGateWorkflow](GreenGateWorkflow.md)
- [PR7720](../entities/PR7720.md) (where this happened)
