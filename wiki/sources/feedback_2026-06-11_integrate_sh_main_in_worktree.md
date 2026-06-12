# Source: integrate.sh MAIN_IN_WORKTREE detection ineffective (2026-06-11)

> **Original capture**: `~/.claude/projects/-Users-jleechan-projects-worktree-misc-23423fg23r2/memory/feedback_2026-06-11_integrate_sh_main_in_worktree.md`
> **Bead**: rev-asntr
> **Type**: feedback (Best Practice)

## Summary

`integrate.sh` is the project's standard "create a fresh branch from main" workflow. Its MAIN_IN_WORKTREE check at line 490 (grep `^branch refs/heads/main$` against `git worktree list --porcelain`) is correct in isolation — returns exit 0 when `main` is in another worktree. But the script still attempts `git checkout main` at line 503 and dies with `fatal: 'main' is already checked out at <other-worktree>`.

## Workaround (verified)

Skip the script and do the worktree-aware equivalent manually:

```bash
git fetch --prune origin main
git -C <worktree-path> checkout -b dev<timestamp> origin/main
# git automatically sets upstream tracking to origin/main
```

Previous branch stays on the remote; the new branch's tip equals `origin/main` HEAD.

## Reusable pattern

When `/integrate` (or any integrate.sh invocation) fails with `fatal: 'main' is already checked out at <other-worktree>`, do NOT try to fix integrate.sh mid-flight. Instead:

1. Fetch origin/main: `git fetch --prune origin main`
2. Create the fresh branch from origin/main in the current worktree: `git checkout -b dev<ts> origin/main`
3. Verify: `git log --oneline -1` shows `origin/main` HEAD as tip
4. Stop the test server if needed: `./test_server_manager.sh stop <old-branch>`

The previous branch stays on the remote and is safe to delete later via GitHub UI or `git push origin --delete <branch>`.

## Why this matters

- The pattern (worktree + main elsewhere) is common in this repo — `worktree_prompt_ignore` is a long-lived worktree holding main.
- A future agent running `/integrate` will hit the same wall.
- A persistent workaround until the integrate.sh detection logic is fixed.

## References

- PR: [#7328](https://github.com/jleechanorg/worldarchitect.ai/pull/7328)
- Bead: rev-asntr
- integrate.sh lines: 488-495 (detection), 501-502 (skip checkout), 856 (create from origin/main)
- Worktrees: `worktree_misc_23423fg23r2`, `worktree_prompt_ignore`
- Related concepts: [[WorktreeWorkflow]], [[GitWorkflow]]
- Prior captures of the same root cause:
  - [integrate.sh main checked out in worktree — workaround (2026-05-23)](integrate-worktree-main-conflict-2026-05-23.md) — original workaround capture
  - [integrate.sh worktree fallback (2026-05-29)](feedback_2026-05-29_integrate_worktree_fallback.md)
  - [ambiguous origin main integrate block](ambiguous-origin-main-integrate-block.md)
