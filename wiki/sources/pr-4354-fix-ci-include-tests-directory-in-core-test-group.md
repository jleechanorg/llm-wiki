---
title: "PR #4354: fix(ci): Include tests/ directory in core test group"
type: source
tags: []
date: 2026-01-31
source_file: raw/prs-worldarchitect-ai/pr-4354.md
sources: []
last_updated: 2026-01-31
---

## Summary
- Fixed CI to run root-level `tests/` directory tests for all core changes
- Previously, `tests/` was not mapped in CI change detection, so utility tests never ran

## Metadata
- **PR**: #4354
- **Merged**: 2026-01-31
- **Author**: jleechan2015
- **Stats**: +14/-567 in 5 files
- **Labels**: none

## Connections
