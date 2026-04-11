---
title: "PR #5995: fix(integrate): skip main checkout when branch is in a worktree"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5995.md
sources: []
last_updated: 2026-03-15
---

## Summary
- `integrate.sh` always tries `git checkout main`, which fails when `main` is checked out in a worktree (git prevents double-checkout of a branch)
- Detects `MAIN_IN_WORKTREE` upfront via `git worktree list --porcelain`
- Skips steps 1-2 (checkout + sync) when main is in a worktree
- Creates new branch from `origin/main` directly instead

## Metadata
- **PR**: #5995
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +23/-2 in 1 files
- **Labels**: none

## Connections
