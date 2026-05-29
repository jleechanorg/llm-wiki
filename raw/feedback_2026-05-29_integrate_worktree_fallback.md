---
name: integrate-worktree-fallback
description: integrate.sh fails when main is checked out in another worktree — use git checkout -b directly from origin/main
type: feedback
bead: none
---

## Rule

**When `integrate.sh` fails with "Fatal: main is already checked out at …", do not retry. Use the direct fallback immediately.**

```bash
git fetch origin main --quiet
git checkout -b dev$(date +%s) origin/main
git branch --set-upstream-to=origin/main <new-branch>
```

## Why

`integrate.sh` attempts `git checkout main` as an intermediate step. In a worktree layout where `main` is checked out in a separate worktree (e.g. `/Users/jleechan/projects/worktree_root_cause`), Git refuses:

```
fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_root_cause'
❌ ERROR: Failed to switch to main
```

The script exits with code 1. No amount of retrying fixes this.

## How to Apply

- When `integrate.sh` exits with the "already checked out" error, immediately switch to the direct fallback.
- Always set upstream right after branch creation (worktree branches don't get it automatically).
- Do NOT try to `git worktree remove` the other checkout — it may be in active use.

## Related

- [[feedback_integrate_worktree]] — earlier captured as "integrate.sh/newbranch.py fail in worktrees; use `git checkout -b <name> origin/main` directly"
- This memory updates that lesson with the exact error string and worktree layout.

## References

- Session 2026-05-29: `/integrate` in `worktree_autolvl_coder`
- Conflicting worktree: `/Users/jleechan/projects/worktree_root_cause`
