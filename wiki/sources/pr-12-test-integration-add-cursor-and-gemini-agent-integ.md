---
title: "PR #12: test(integration): add cursor and gemini agent integration tests"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-12.md
sources: []
last_updated: 2026-03-16
---

## Summary
Adds real integration tests for cursor-agent and gemini CLI plugins.

**Proved green locally (8/8 pass):**
- agent-cursor: 4/4 (isProcessRunning alive/exited, file created, fibonacci correct)
- agent-gemini: 4/4 (same assertions)

**Key details:**
- cursor: uses `--print --yolo`; skips if not authenticated
- gemini: passes `GEMINI_API_KEY` explicitly via tmux env
- Both auto-skip when prerequisites are missing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -

## Metadata
- **PR**: #12
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +827/-514 in 12 files
- **Labels**: none

## Connections
