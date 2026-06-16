---
name: git-reset-wrong-branch-orphans-commits
description: "`git reset --hard` on a branch other than the intended target orphans all commits unique to that branch; recovery is possible via reflog + object store within gc window."
metadata: 
  node_type: memory
  type: feedback
  classification: Critical
  originSessionId: d61bbeb8-6157-4234-81da-4a9e2432120d
---

# `git reset --hard` on the wrong branch orphans commits

## What happened
While on `feat/hooks-and-disk-magician-scopes` (with 2 unpushed commits 7763aeb20 + 93a979dfb),
I ran `git reset --hard origin/main` to align main with origin. The reset ran on the **current**
branch (feat), not main, so feat's HEAD moved to origin/main's tip and the 2 unpushed commits
were orphaned (still in object store + reflog, but no longer reachable from any branch).

## Recovery
Both commits were still in `.git/objects/` and the reflog retained the history. The fix:

```bash
git -C /Users/jleechan/projects_other/user_scope reflog --all | grep -E "7763aeb20|93a979dfb"
# found at refs/heads/feat/...@{N}: commit: ...
git branch -f feat/hooks-and-disk-magician-scopes 93a979dfb   # restore pointer, no working-tree churn
```

Recovery is only possible before `git gc` runs (default 14 days, 2 weeks for unreachable objects).
A `git prune --expire=now` would have destroyed the orphans permanently.

## Why this rule
The working tree is always tied to ONE branch. `git reset --hard <ref>` mutates that branch.
The intent ("align main with origin") requires first `git checkout main`, then reset.

## The correct sequence (memorize this)
```bash
# WRONG (resets whatever branch is currently checked out):
git reset --hard origin/main            # ← I did this on feat

# RIGHT (explicit checkout, then reset on the target branch):
git checkout main
git reset --hard origin/main            # main is the current branch, so this is safe

# OR — when no working-tree change is wanted at all:
git branch -f main origin/main          # moves the branch pointer only, no checkout
```

## When this matters most
- After merging a PR and wanting to fast-forward main: ALWAYS `git checkout main` first
- After a rebase in a worktree: the worktree's branch is the one being mutated (safe)
- After pulling: `git pull --ff-only` is the safe form; `--rebase` is also safe (rebases current branch)

## Recovery checklist if it happens
1. **Do NOT run `git gc` or `git prune`** — they destroy unreachable objects
2. `git reflog --all | grep <lost-sha>` — if found, `git branch -f <name> <sha>` restores it
3. `git fsck --no-reflogs --lost-found` — finds orphans even after reflog expiry
4. If fsck returns nothing, the commits are gone for good; check pack-files in `.git/objects/pack/`

## Related
- [[feedback_verify_before_reporting]] — run `git log feat/<name>` before AND after reset to verify
- [[project_2026-06-12_regrowth_prevention_prs]] — the disk_magician work also used `git reset --hard`
  to align worktrees; always paired with explicit checkout there
