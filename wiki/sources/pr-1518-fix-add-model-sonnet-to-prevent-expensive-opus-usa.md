---
title: "PR #1518: fix: Add --model sonnet to prevent expensive Opus usage in agent monitor"
type: source
tags: []
date: 2025-09-01
source_file: raw/prs-worldarchitect-ai/pr-1518.md
sources: []
last_updated: 2025-09-01
---

## Summary
- Adds `--model sonnet` to Claude CLI invocation in `agent_monitor.py`
- Prevents expensive Opus model usage during automatic agent restarts
- Fixes cost issue observed on Aug 31st (~$823 in unexpected Opus usage)

## Metadata
- **PR**: #1518
- **Merged**: 2025-09-01
- **Author**: jleechan2015
- **Stats**: +74/-74 in 1 files
- **Labels**: none

## Connections
