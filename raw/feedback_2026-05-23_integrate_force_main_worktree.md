---
name: integrate-force-main-checked-out-in-worktree
description: integrate --force needed when main is checked out in a worktree
type: feedback
bead: none
---

## integrate --force needed when main is checked out in a worktree

**Classification**: Best Practice
**Date**: 2026-05-23

### Context
Running `/integrate` on branch `duplicate-report-recent-links` failed because `main` is checked out at `/Users/jleechan/projects/worktree_root_cause`. The integrate script detected this and blocked the checkout.

### Technical Detail
- `main` branch checked out in worktree at `/Users/jleechan/projects/worktree_root_cause`
- `integrate.sh` refuses to switch to `main` when already checked out elsewhere
- Using `--force` flag bypasses this safety and creates branch from `origin/main` directly
- The branch `duplicate-report-recent-links` was force-pushed to sync before deletion (was 5 commits behind remote after upstream merges)

### Solution
```bash
./integrate.sh --force
```
This skips the main checkout and creates the new branch from `origin/main` directly.

### Also Changed
- `claudem()` in `~/.bashrc`: changed `--effort xhigh` to `--effort high` as default
- This affects the MiniMax API route via `https://api.minimax.io/anthropic`

### Verification
Integration completed successfully, branch `dev1779576936` created from `origin/main`.

### References
- Branch `duplicate-report-recent-links` force-pushed to sync with remote (SHA: f5f1d44efc)
- Worktree root cause at `/Users/jleechan/projects/worktree_root_cause`