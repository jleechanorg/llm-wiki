---
title: "PR #1: WORKING: Fix split CWD inheritance and bash job spam"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2026-03-05
---

## Summary
- **Split CWD inheritance**: New split panes now inherit the working directory from the source panel (`panelDirectories[panelId]` → `currentDirectory` fallback chain)
- **Bash job spam fix**: Suppress `[N] Done ...` notifications from background shell integration probes via `& disown`
- **Integration test**: Added `tests/test_split_cwd_inheritance.py` to verify split and tab CWD inheritance via real sockets

## Metadata
- **PR**: #1
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +215/-3 in 4 files
- **Labels**: none

## Connections
