---
title: "PR #5965: feat(mem0): UserPromptSubmit+Stop hooks for automatic memory recall/save"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5965.md
sources: []
last_updated: 2026-03-15
---

## Summary
- `mem0_recall.py` — fires on `UserPromptSubmit`, searches `openclaw_mem0` qdrant, injects top-6 memories as `additionalContext` before every prompt
- `mem0_save.py` — fires on `Stop`, extracts facts from last response via mem0 LLM, saves to qdrant

## Metadata
- **PR**: #5965
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +229/-0 in 3 files
- **Labels**: none

## Connections
