---
name: integrate command cleanup behavior
description: integrate.sh deletes synced merged branch, uses origin/main when main is in worktree
type: feedback
bead: none
originSessionId: 62bb3693-a282-4bf6-987e-ef9362e465b5
---
## Context
Running `/integrate` on `chore/disable-skeptic-cron` which had:
- PR #6830 merged to main
- Branch was synced with remote (`origin/chore/disable-skeptic-cron`)
- Clean working tree (all commits already on main)

## What happened
1. `integrate.sh` detected the branch was synced and had a merged PR
2. It created a new timestamp-based branch `dev1778136280` from `origin/main`
3. It deleted the old `chore/disable-skeptic-cron` branch after the new branch was created
4. Since `main` is checked out in a worktree (`/Users/jleechan/projects/worktree_goal2`), the script skipped local checkout and used `origin/main` as the base

## Key technical details

### integrate.sh behavior
- **Branch deletion**: A synced branch with a merged PR is deleted after new branch creation — this is safe and correct
- **Worktree detection**: When `main` is checked out in a worktree, the script skips `git checkout main` and uses `origin/main` directly
- **Branch naming**: No argument → `dev{timestamp}` (e.g., `dev1778136280`); argument → custom name
- **Unmerged branch check**: The script checks before deleting — only deletes if safe

### Pre-integration artifact cleanup (lesson from this session)
Before running `/integrate` or pushing a branch, always check for stray files not in `origin/main`:
```bash
git diff origin/main --name-only | head -20
```
A stray `specs/skeptic-report.json` was in the local branch (from a skeptic run) but not in `origin/main`. It was removed via `git rm` + amend before push.

**Rule**: Any file in the working tree that doesn't exist in `origin/main` and isn't intentionally added should be removed before push. Stray artifacts cause CI confusion and add noise to PRs.

### PR creation after push
`gh pr list --head <branch>` returned nothing even though PR #6830 existed — because the branch was deleted after merge. When re-creating a PR for a re-born branch name, `gh pr create` works normally.

## Pattern
- **Safe cleanup flow**: Synced + merged branch → integrate → new branch from main + old branch deleted
- **Worktree constraint**: main in worktree → script uses `origin/main` directly, doesn't try to checkout
- **Artifact rule**: `git diff origin/main --name-only` before push to catch stray files

## Verification
- New branch: `dev1778136280` — clean, tracking `origin/main`, no diff vs origin/main
- Old branch deleted: `chore/disable-skeptic-cron` (was 7bc85a9ca)
- PR #6830 merged before branch deletion

## References
- `/integrate` command: `.claude/commands/integrate.md`
- integrate.sh: repo root `integrate.sh`