---
name: integrate-sh-fails-when-main-checked-out-in-another-worktree
description: integrate.sh fails when main is checked out in another worktree - workaround is manual fetch + checkout
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 973b6da6-a6fe-403a-a4cf-951ee81c54ca
---

## integrate.sh fails when main is checked out in another worktree

### Context
- Ran `/integrate` on `worktree_misc875675` (current branch: `dev1779583582`)
- integrate.sh tried to switch to `main` but failed because `main` is already checked out at `worktree_root_cause`
- Error: `fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_root_cause'`

### Root Cause
Git worktree constraint: a branch can only be checked out in one worktree at a time. When `main` is checked out in `worktree_root_cause`, integrate.sh cannot switch the `worktree_misc875675` session to `main`.

### Solution
Manual workaround - don't use integrate.sh when main is checked out elsewhere:

```bash
git fetch origin main
git checkout -b dev<timestamp> origin/main
git branch --set-upstream-to=origin/main
```

This creates a new branch from the fetched `origin/main` without attempting to switch the current worktree to `main`.

### Files
- `integrate.sh` - attempted but failed
- `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/` - memory dir

### References
- integrate.sh cannot switch to main when another worktree has it checked out
- related feedback: `feedback_2026-04-25_integrate_worktree_main_conflict.md`