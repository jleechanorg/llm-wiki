---
title: "PR #1248: fix: Restore Claude Code hooks functionality - UserPromptSubmit and speculation detection"
type: source
tags: []
date: 2025-08-10
source_file: raw/prs-worldarchitect-ai/pr-1248.md
sources: []
last_updated: 2025-08-10
---

## Summary
Fixes critical Claude Code hooks configuration issues that broke slash command composition and hook execution timing:

- **Restore UserPromptSubmit hooks**: Re-enables `compose-commands.sh` for slash command combinations like `/think /debug /analyze`
- **Fix speculation detection hook timing**: Move from PostResponse to PostToolUse for proper execution
- **Remove incorrect PreToolUse usage**: UserPromptSubmit is the correct hook for user input processing

## Metadata
- **PR**: #1248
- **Merged**: 2025-08-10
- **Author**: jleechan2015
- **Stats**: +13/-3 in 1 files
- **Labels**: none

## Connections
