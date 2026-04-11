---
title: "PR #1: feat: Add functional integration tests for real Claude/Cursor agents"
type: source
tags: []
date: 2025-12-17
source_file: raw/prs-/pr-1.md
sources: []
last_updated: 2025-12-17
---

## Summary
- Added real CLI integration tests that invoke actual Claude and Cursor CLIs
- Refactored test harness with Template Method pattern - child classes only define CLI config
- Tests verify full telemetry pipeline: CLI → Redis → SQLite

## Metadata
- **PR**: #1
- **Merged**: 2025-12-17
- **Author**: jleechan2015
- **Stats**: +1078/-0 in 10 files
- **Labels**: none

## Connections
