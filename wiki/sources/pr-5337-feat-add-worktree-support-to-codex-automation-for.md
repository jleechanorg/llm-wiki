---
title: "PR #5337: feat: Add worktree support to Codex automation for any-repo compatibility"
type: source
tags: []
date: 2026-02-13
source_file: raw/prs-worldarchitect-ai/pr-5337.md
sources: []
last_updated: 2026-02-13
---

## Summary
Enable Codex automation to work from any directory by using git worktrees in `/tmp`, fixing the "not a git repository" errors that prevented PR creation.

**Key themes:**
- Worktree-based isolation - eliminates directory dependency
- Repository auto-detection - works with any configured repo
- Cleanup automation - prevents /tmp pollution

## Metadata
- **PR**: #5337
- **Merged**: 2026-02-13
- **Author**: jleechan2015
- **Stats**: +817/-189 in 7 files
- **Labels**: none

## Connections
