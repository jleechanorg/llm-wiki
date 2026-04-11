---
title: "PR #961: fix: Add context-aware message selection to prevent Cerebras context overflow"
type: source
tags: []
date: 2026-01-04
source_file: raw/prs-/pr-961.md
sources: []
last_updated: 2026-01-04
---

## Summary
Fixed single message mode failing with Cerebras 400 error when conversations exceeded 131K token limit. Implemented context-aware message selection with proper priority ordering.

## Metadata
- **PR**: #961
- **Merged**: 2026-01-04
- **Author**: jleechan2015
- **Stats**: +304/-32 in 4 files
- **Labels**: none

## Connections
