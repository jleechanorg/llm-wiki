---
title: "PR #6111: sync: update claude commands and hooks from user-scope"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldarchitect-ai/pr-6111.md
sources: []
last_updated: 2026-04-06
---

## Summary
Syncs 5 files from user-scope config backup to worldarchitect.ai `.claude/`:

- **`compose-commands.sh`**: idle hook guard, worktree NO-PR sentinel, CR review staleness detection, silent passthrough (no UI banner when prompt is unmodified)
- **`UserPromptSubmit.sh`**: suppression sentinel, `find_conversation_file`, PR merge-state guard, session health thresholds (500/1000/2000 messages)
- **`claw.md`**: rewritten for OpenClaw native WebSocket dispatch via `openclaw agent` CLI
- **`exportcommands

## Metadata
- **PR**: #6111
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +1311/-59 in 5 files
- **Labels**: none

## Connections
