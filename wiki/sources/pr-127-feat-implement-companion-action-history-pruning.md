---
title: "PR #127: feat: implement companion action history pruning"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-127.md
sources: []
last_updated: 2026-03-29
---

## Summary
Companion action history in `companion_actions` SQLite table was growing indefinitely with each tick cycle. Without pruning, long-running campaigns would accumulate thousands of action rows, degrading query performance and narration quality.

## Metadata
- **PR**: #127
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +403/-99 in 8 files
- **Labels**: none

## Connections
