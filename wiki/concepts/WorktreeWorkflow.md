# WorktreeWorkflow

Workflow conventions for working in a git worktree where `main` is checked out in another worktree (a common pattern in long-lived development environments where the main worktree holds `main` and feature work happens in dedicated worktrees).

## Key conventions

- **Do not `git checkout main` from a non-main worktree** — git refuses with `fatal: 'main' is already checked out at <other-worktree>`. Always create a new branch from `origin/main` instead.
- **Use `git checkout -b <branch> origin/main`** in the current worktree to start a new branch without touching main. Git automatically sets upstream tracking to `origin/main`.
- **The previous branch stays on the remote** (if previously pushed) and is not deleted locally until the worktree itself is removed. Safe to delete later via `git push origin --delete <branch>` or GitHub UI.
- **Verify with `git log --oneline -1`** that the new branch's tip equals `origin/main` HEAD (`git rev-parse origin/main`).

## Failure mode: integrate.sh MAIN_IN_WORKTREE detection

`integrate.sh` is documented to handle the worktree case (lines 488-495), but in practice the detection does NOT work and the script falls through to the `git checkout main` step at line 503. This produces:

```
1. Switching to main branch...
   Checkout error details:
fatal: 'main' is already checked out at '/path/to/other-worktree'
```

**Workaround**: do not invoke integrate.sh from a worktree where main is in another worktree. Instead, perform the equivalent steps manually:

```bash
git fetch --prune origin main
git -C <worktree-path> checkout -b dev<timestamp> origin/main
# Test server stop (if applicable): ./test_server_manager.sh stop <old-branch>
```

The script's MAIN_IN_WORKTREE path (line 856) is functionally identical — it does `git -c core.hooksPath="$GIT_HOOKS_PATH" checkout -b "$branch_name" origin/main`.

## Test server cleanup

Some worktrees include `./test_server_manager.sh` for stopping/starting per-branch test servers. Check if present in the worktree root before relying on it.

## Related concepts

- [[GitWorkflow]]
- [[NoWorktreeIsolation]]
- [[GitSHATracking]]

## Sources

- [feedback_2026-06-11_integrate_sh_main_in_worktree](../sources/feedback_2026-06-11_integrate_sh_main_in_worktree.md) — initial capture from PR #7328 integrate failure
