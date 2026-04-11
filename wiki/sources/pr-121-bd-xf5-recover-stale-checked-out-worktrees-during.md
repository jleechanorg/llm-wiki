---
title: "PR #121: bd-xf5: recover stale checked-out worktrees during spawn"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-121.md
sources: []
last_updated: 2026-03-23
---

## Summary
AO spawns can fail with git exit 128 when a target branch is still registered as checked out in an abandoned worktree. The current worktree plugin retries checkout for existing branches, but does not recover stale worktrees that no longer have an active tmux session.

## Metadata
- **PR**: #121
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +121/-11 in 3 files
- **Labels**: none

## Connections
