---
description: integrate.sh fails when main is checked out in another worktree - manual workaround
type: source
tags: [git, worktree, integration, workflow]
---

# integrate.sh fails when main checked out in another worktree

## Source

Captured from: `/integrate` execution on `worktree_misc875675` (2026-05-23)

## Problem

integrate.sh cannot switch to `main` when `main` is already checked out in another worktree (worktree_root_cause):

```
fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_root_cause'
```

## Root Cause

Git worktree constraint: a branch can only be checked out in one worktree at a time.

## Workaround

```bash
git fetch origin main
git checkout -b dev<timestamp> origin/main
git branch --set-upstream-to=origin/main
```

## References

- Related: `feedback_2026-05-22_integrate_worktree_safe_pattern.md` (prior same issue)