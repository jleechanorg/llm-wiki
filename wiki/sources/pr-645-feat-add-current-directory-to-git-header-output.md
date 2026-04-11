---
title: "PR #645: feat: Add current directory to git header output"
type: source
tags: []
date: 2025-07-17
source_file: raw/prs-worldarchitect-ai/pr-645.md
sources: []
last_updated: 2025-07-17
---

## Summary
- Add directory detection logic to git-header.sh to show current working directory relative to git root
- Display "root" when at git root, otherwise show relative path (e.g., "worktree_roadmap") 
- Include `Dir:` field in all header output formats for better context awareness

## Metadata
- **PR**: #645
- **Merged**: 2025-07-17
- **Author**: jleechan2015
- **Stats**: +15/-5 in 2 files
- **Labels**: none

## Connections
