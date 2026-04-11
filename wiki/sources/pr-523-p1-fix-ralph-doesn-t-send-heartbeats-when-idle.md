---
title: "PR #523: [P1] fix: ralph doesn't send heartbeats when idle"
type: source
tags: []
date: 2026-04-06
source_file: raw/prs-worldai_claw/pr-523.md
sources: []
last_updated: 2026-04-06
---

## Summary
Ralph sessions were being flagged as stuck or killed by the orchestrator because they weren't responding to heartbeat polls. This happened because ralph runs agents (like Claude Code) by piping input, which prevents the agent from seeing interactive heartbeat polls typed into the tmux pane.

## Metadata
- **PR**: #523
- **Merged**: 2026-04-06
- **Author**: jleechan2015
- **Stats**: +131/-4 in 3 files
- **Labels**: none

## Connections
