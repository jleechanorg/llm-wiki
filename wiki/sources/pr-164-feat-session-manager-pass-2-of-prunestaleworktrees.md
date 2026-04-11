---
title: "PR #164: feat(session-manager): Pass 2 of pruneStaleWorktrees cleans zombie worktrees outside ~/.worktrees/"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-164.md
sources: []
last_updated: 2026-03-24
---

## Summary
- **Bug**: `pruneStaleWorktrees` only scanned `~/.worktrees/{projectId}/` directories, leaving zombie worktrees at custom paths (e.g. `/tmp/pr-360-worktree`) behind after AO session death
- **Fix**: Added Pass 2 to `pruneStaleWorktrees` that uses `git worktree list --porcelain` to enumerate ALL registered worktrees per project, then removes zombies whose AO sessions are in a terminal state (`killed`, `merged`, `done`, etc.)
- Guards with the AO session name pattern so human-created worktrees are

## Metadata
- **PR**: #164
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +308/-22 in 2 files
- **Labels**: none

## Connections
