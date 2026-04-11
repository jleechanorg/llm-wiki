---
title: "PR #975: Enhance /bclean command with comprehensive worktree cleanup functionality"
type: source
tags: []
date: 2025-07-26
source_file: raw/prs-worldarchitect-ai/pr-975.md
sources: []
last_updated: 2025-07-26
---

## Summary
This PR enhances the `/bclean` command by adding comprehensive worktree cleanup functionality, addressing a significant gap in the current Git workspace cleanup tool.

### Key Enhancements

- ✅ **Worktree Cleanup**: Automatically detects and removes stale worktrees based on commit age
- ✅ **Configurable Age Threshold**: New `--days N` parameter (default: 2 days)  
- ✅ **Safety First**: Preserves worktrees with uncommitted changes
- ✅ **Consistent UI**: Maintains same color coding and confirmatio

## Metadata
- **PR**: #975
- **Merged**: 2025-07-26
- **Author**: jleechan2015
- **Stats**: +199/-49 in 2 files
- **Labels**: none

## Connections
