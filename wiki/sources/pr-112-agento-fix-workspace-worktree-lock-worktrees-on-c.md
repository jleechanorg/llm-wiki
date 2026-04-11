---
title: "PR #112: [agento] fix(workspace-worktree): lock worktrees on create/restore to prevent accidental prune"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-112.md
sources: []
last_updated: 2026-03-23
---

## Summary
Without worktree locking, git worktree prune can silently delete a live AO workspace if its directory is removed while the session is still active. AOs destroy() already called git worktree remove --force, but unlocked worktrees are also vulnerable to accidental deletion by git pull, git gc, or manual git worktree prune runs.

Root cause: workspace-worktree plugin called git worktree add but never followed up with git worktree lock.

Closes bd-diq

## Metadata
- **PR**: #112
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +143/-15 in 3 files
- **Labels**: none

## Connections
