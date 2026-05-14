# integrate.sh Fails With Unrelated Histories on Diverged Main

## Problem

When local `main` diverges from `origin/main`, `integrate.sh --force` attempts a merge that fails with "refusing to merge unrelated histories". The script has no `--reset` or `--hard-reset` option.

## Root Cause

The divergence detection in `integrate.sh` correctly identifies the split but its force-mode resolution path uses `git merge origin/main`, which fails when git considers the histories unrelated. This occurs when local main has drifted significantly from the remote.

## Resolution

Bypass `integrate.sh` entirely:

```bash
git checkout main
git reset --hard origin/main
git checkout -b dev$(date +%s)
git branch -D <old-branch>
```

## When This Applies

- `integrate.sh` reports "DIVERGENCE DETECTED" and "refusing to merge unrelated histories"
- The local branch has no unique work (all commits are in main's ancestry)
- You need a clean starting point from latest main

## Verification

- `git log --oneline -3` confirms HEAD matches origin/main
- New branch created from latest main HEAD
