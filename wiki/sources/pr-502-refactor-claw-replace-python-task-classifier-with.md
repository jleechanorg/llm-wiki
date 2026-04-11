---
title: "PR #502: refactor(claw): replace Python task-classifier with LLM judgment"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldai_claw/pr-502.md
sources: []
last_updated: 2026-04-05
---

## Summary
- Remove Python inline script for task classification (coding vs read_only)
- Remove Python inline script for ISSUE_ID extraction from task description
- Replace both with LLM judgment (the LLM already has full context)
- Reduces shell complexity and removes fragile regex matching

## Metadata
- **PR**: #502
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +26/-75 in 1 files
- **Labels**: none

## Connections
