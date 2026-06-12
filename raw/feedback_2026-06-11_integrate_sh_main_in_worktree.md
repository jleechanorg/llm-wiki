---
name: integrate.sh MAIN_IN_WORKTREE detection ineffective
description: integrate.sh fails with "main already checked out" when run from a worktree even though its MAIN_IN_WORKTREE check returns true in isolation
type: feedback
bead: rev-asntr
---

# integrate.sh MAIN_IN_WORKTREE detection does not work as designed

## Context

`integrate.sh` is the project's standard "create a fresh branch from main" workflow. It is documented to handle the case where `main` is checked out in another worktree (line 488-495 sets `MAIN_IN_WORKTREE=true` when `git worktree list --porcelain` shows `branch refs/heads/main` for any worktree). When `MAIN_IN_WORKTREE=true`, the script skips the `git checkout main` step (line 501-502) and uses `origin/main` as the branch base.

## Failure observed (2026-06-11)

Running `./integrate.sh` from worktree `worktree_misc_23423fg23r2` (current branch: `feat/feat-duplicate-campaign-button-add-a-duplicate-campaign-butt`) where `main` is checked out in `worktree_prompt_ignore`:

```
✅ Branch 'feat/feat-duplicate-campaign-button-add-a-duplicate-campaign-butt' is synced with remote and will be deleted after integration
1. Switching to main branch...
   Checkout error details:
fatal: 'main' is already checked out at '/Users/jleechan/projects/worktree_prompt_ignore'
```

The MAIN_IN_WORKTREE check should have caught this. Testing the exact same grep from the same shell returned `EXIT=0` (match found). Yet the script still executed the line-503 `git checkout main` path.

## Workaround (used)

Manually performed the equivalent of the script's MAIN_IN_WORKTREE=true branch (line 856) without going through integrate.sh:

```bash
git -C <worktree-path> checkout -b dev<timestamp> origin/main
# git already sets upstream tracking to origin/main automatically
```

This creates the new branch in the current worktree, switches to it, and the previous branch is left on the remote (not deleted locally — it's still a checked-out ref until the worktree is removed). No need for `git checkout main` at all.

## Why this matters

- The user explicitly invoked `/integrate` expecting the standard workflow. The script's failure mode produced confusing output and required manual diagnosis.
- The pattern (`integrate.sh` + worktree where main is elsewhere) is common in this repo — `worktree_prompt_ignore` is a long-lived worktree holding main.
- A future agent running `/integrate` will hit the same wall.

## Reusable pattern

When `/integrate` (or any integrate.sh invocation) fails with `fatal: 'main' is already checked out at <other-worktree>`, do NOT try to fix integrate.sh mid-flight. Instead:

1. Fetch origin/main: `git fetch --prune origin main`
2. Create the fresh branch from origin/main in the current worktree: `git checkout -b dev<ts> origin/main`
3. Verify: `git log --oneline -1` shows `origin/main` HEAD as tip
4. Stop the test server if needed: `./test_server_manager.sh stop <old-branch>` (only present in some worktrees)

The previous branch stays on the remote and is safe to delete later via GitHub UI or `git push origin --delete <branch>`.

## Verification

- `git rev-parse --show-toplevel` confirmed the new branch's tip = `origin/main` HEAD (`2cca3481dc`)
- `git status --short` showed only untracked test artifacts (not committed code), so no carry-over
- No force mode needed; clean creation succeeded in one step

## Open follow-up

The actual root cause of why MAIN_IN_WORKTREE was false in the script run despite the grep working in isolation is not pinned down. Possible candidates: subshell variable scoping, `set -e` exiting before the assignment, or a race with `git fetch --prune` at line 354 touching the worktree metadata. Filing as a follow-up to fix integrate.sh rather than working around it.

## References

- PR: [#7328](https://github.com/jleechanorg/worldarchitect.ai/pull/7328) (duplicate campaign button — the work that triggered this integrate)
- Bead: rev-asntr
- integrate.sh lines: 488-495 (detection), 501-502 (skip checkout), 856 (create from origin/main)
- Worktrees involved: `worktree_misc_23423fg23r2` (origin of integrate.sh call), `worktree_prompt_ignore` (where main lives)
