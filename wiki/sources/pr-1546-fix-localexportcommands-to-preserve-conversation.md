---
title: "PR #1546: 🚨 Fix /localexportcommands to preserve conversation history"
type: source
tags: []
date: 2025-09-05
source_file: raw/prs-worldarchitect-ai/pr-1546.md
sources: []
last_updated: 2025-09-05
---

## Summary
🚨 **CRITICAL FIX**: The `/localexportcommands` command was destructively replacing the entire `~/.claude` directory, destroying conversation history stored in `projects/`. This caused users to lose thousands of dollars worth of API usage data.

### Root Cause
- `/localexportcommands` moved entire `~/.claude` directory to backup
- Replaced it with only project's `.claude` folder contents  
- **Result**: All conversation history JSONL files were lost
- User lost ~$4000 worth of conversation data (

## Metadata
- **PR**: #1546
- **Merged**: 2025-09-05
- **Author**: jleechan2015
- **Stats**: +77/-45 in 1 files
- **Labels**: none

## Connections
