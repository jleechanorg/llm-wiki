# integrate --force for worktree main checkout

**Date**: 2026-05-23
**Type**: workflow
**Classification**: Best Practice

## Problem

Running `/integrate` failed when `main` branch is checked out in another worktree (`/Users/jleechan/projects/worktree_root_cause`). The integrate script blocks checkout of `main` if already checked out elsewhere.

## Solution

Use `--force` flag to bypass the safety check:

```bash
./integrate.sh --force
```

This creates the new branch from `origin/main` directly without requiring a local `main` checkout.

## Also Changed

- `claudem()` in `~/.bashrc`: `--effort xhigh` → `--effort high` (default MiniMax effort level)

## References

- Branch `dev1779576936` created after cleanup of `duplicate-report-recent-links`
- `duplicate-report-recent-links` force-pushed to sync with remote (SHA: f5f1d44efc)