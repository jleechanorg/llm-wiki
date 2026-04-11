---
title: "PR #1285: Fix create_worktree.sh to navigate to existing directory instead of exiting"
type: source
tags: []
date: 2025-08-13
source_file: raw/prs-worldarchitect-ai/pr-1285.md
sources: []
last_updated: 2025-08-13
---

## Summary
- Fixed create_worktree.sh to cd into existing directory instead of exiting terminal
- Changed error_exit to graceful navigation when worktree directory already exists
- Maintains consistent success message format and user experience
- Prevents unwanted terminal exit behavior

## Metadata
- **PR**: #1285
- **Merged**: 2025-08-13
- **Author**: jleechan2015
- **Stats**: +31/-2 in 1 files
- **Labels**: none

## Connections
