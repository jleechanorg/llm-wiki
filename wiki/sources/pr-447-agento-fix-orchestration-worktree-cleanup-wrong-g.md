---
title: "PR #447: [agento] fix(orchestration): worktree cleanup wrong grep key + wrong remove path (orch-tzc)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-447.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Fixed `get_registered_worktrees()` to parse the correct git porcelain key: `"worktree /path"` instead of `"path /path"` (wrong grep key bug)
- Fixed `cleanup_zombie_worktree()` to pass the checkout directory path to `git worktree remove` instead of the metadata dir path (wrong path bug)
- These bugs caused zombie worktree entries at `/private/tmp/pr-XXX-worktree` to persist every cycle, blocking `ao spawn --claim-pr` with "already checked out" errors

## Metadata
- **PR**: #447
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +567/-0 in 4 files
- **Labels**: none

## Connections
