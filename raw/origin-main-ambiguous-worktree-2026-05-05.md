# origin/main ambiguous ref in worktrees causes integrate failure

**Date**: 2026-05-05
**Type**: Git workflow anti-pattern

## Problem

When a local branch `refs/heads/origin/main` shadows the remote tracking ref `refs/remotes/origin/main`, `git checkout` and `./integrate.sh` fail with:

```
fatal: ambiguous object name: 'origin/main'
```

The worktree was in detached HEAD state at an unrelated commit (`2089d342d`) and was 554 commits ahead of `origin/main`.

## Root Cause

Two refs with the same short name exist:
- `refs/heads/origin/main` → local branch at `733a44f186a7ce51e00abee76155c47a689e7ffb`
- `refs/remotes/origin/main` → remote tracking branch at `f22bc0ad0c474fb79c699b843aec12fcdbcb6d1b`

Git resolves `origin/main` ambiguously between them.

## Resolution

1. Get actual remote SHA: `git ls-remote origin main`
2. Create branch directly from SHA: `git checkout -b dev{timestamp} f22bc0ad0c474fb79c699b843aec12fcdbcb6d1b`

Alternative: `git branch -D origin/main` to remove the confusing local branch.

## Context

This occurred after PR #6801 was merged, when attempting to run `./integrate.sh` to create a fresh integration branch. The worktree had accumulated many local branches with namespace collisions.
