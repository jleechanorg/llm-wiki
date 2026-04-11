---
title: "PR #1491: Fix create_worktree.sh to create sibling worktrees"
type: source
tags: [bug]
date: 2025-08-28
source_file: raw/prs-worldarchitect-ai/pr-1491.md
sources: []
last_updated: 2025-08-28
---

## Summary
- Modified `create_worktree.sh` script to create sibling worktrees instead of child directories
- Changed directory structure from `./worktree_name/` to `../worktree_name/`
- Updated all path references and collision checks accordingly
- Verified script works properly when sourced for directory navigation

## Metadata
- **PR**: #1491
- **Merged**: 2025-08-28
- **Author**: jleechan2015
- **Stats**: +13/-12 in 1 files
- **Labels**: bug

## Connections
