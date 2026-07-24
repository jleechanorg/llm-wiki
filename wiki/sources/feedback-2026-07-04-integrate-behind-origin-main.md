---
title: "integrate.sh hard-stop when branch is behind origin/main (4th case)"
type: source
tags: [git-workflow, integrate.sh, safety, worktree]
date: 2026-07-04
source_file: ../../.claude/projects/-Users-jleechan--hermes/memory/feedback_2026-07-04_integrate_behind_origin_main.md
---

## Summary
`./integrate.sh` hard-stops when the current branch is N commits BEHIND `origin/main` (4th case not covered by jleechan-9o99 decision matrix which only listed "local commits ahead"). Safe workaround: `git reset --hard origin/main` after confirming zero local-only commits via `git log --oneline origin/main..HEAD`. Alternative when main is checked out in another worktree: skip the script's `git checkout main` step and run `git checkout -b dev$(date +%s) origin/main` directly.

## Key Claims
- integrate.sh has 5 hard-stops (4 known + 1 newly documented here): uncommitted changes, local-only commits ahead, unmerged integration PRs, `git checkout main` failure, **branch N commits behind origin/main** (this entry)
- The "branch N behind" case is safe to reset IF `git log --oneline origin/main..HEAD` returns empty (no local-only commits to lose)
- The existing jleechan-9o99 decision matrix does not explicitly cover the "behind" case — operators can confuse it with "ahead"
- The 16-commits-behind case in this session was the merged PRs #734, #736, #737 (openclaw kill + cron wrapper + scrub)

## Key Quotes
> "HARD STOP: Branch 'fix/health-alert-false-alarms' is not synced with remote 'origin/main':
>   • Local commits ahead: 0
>   • Remote commits ahead: 16"

> "`--force` mode stashes uncommitted but still hard-stops on the sync gap (verified)."

## Connections
- [[IntegrateHardStop]] — parent topic (jleechan-9o99 4-case decision matrix)
- [[IntegrateWorktreeMainConflict]] — 2026-05-23 first occurrence of "main in another worktree" blocker
- [[IntegrateBranchMismatch]] — branch-name-mismatch sibling
- [[GitResetWrongBranchOrphans]] — anti-pattern this lesson reinforces (verify zero local commits before reset)
- [[WorktreeIsolation]] — CLAUDE.md rule this workflow obeys
- [[MergeSafety]] — `--force` analog: never bypass without explicit human approval

## Reusable pattern
```bash
# Verify zero local-only commits (REQUIRED before reset)
git log --oneline origin/main..HEAD   # must be empty

# Reset branch to origin/main (safe when 0 local commits)
git reset --hard origin/main

# Re-run integrate.sh — passes sync check
./integrate.sh

# OR if main lives in another worktree, create branch directly:
git checkout -b dev$(date +%s) origin/main
git checkout -- <runtime-churn-file>  # e.g., cron/jobs.json
```