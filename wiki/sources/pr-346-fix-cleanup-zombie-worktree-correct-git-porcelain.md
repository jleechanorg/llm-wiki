---
title: "PR #346: fix: cleanup_zombie_worktree — correct git porcelain parsing, add tests"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-346.md
sources: []
last_updated: 2026-03-21
---

## Summary
- **Bug fix**: `cleanup_zombie_worktree` in `ao-pr-poller.sh` silently failed to remove stale worktrees because the grep key was wrong (`^path $wt_path` vs git's actual `worktree /path` porcelain format) and it passed metadata dir paths to `git worktree remove` instead of actual checkout paths.
- **Test added**: `ao-pr-poller-worktree-cleanup-test.sh` — 5 unit tests covering the awk path extraction, main-worktree safety guard, empty-not-found case, old buggy grep regression, and tmux kill loop.

## Metadata
- **PR**: #346
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +823/-0 in 2 files
- **Labels**: none

## Connections
