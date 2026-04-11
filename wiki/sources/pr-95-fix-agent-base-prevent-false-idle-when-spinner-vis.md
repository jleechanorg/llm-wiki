---
title: "PR #95: fix(agent-base): prevent false-idle when spinner visible above ❯ prompt (orch-jtc7)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-95.md
sources: []
last_updated: 2026-03-23
---

## Summary
AO session monitor calls detectActivity → classifyTerminalOutput to determine if an agent is working. Claude Code and Gemini CLI render a ❯ prompt glyph at the bottom of the terminal buffer even while thinking/using tools above it. The old code checked only the last line: if it was ❯, it unconditionally returned "idle".

This caused false IDLE reactions and premature needs_input signals between tool calls (bead: orch-jtc7).

## Metadata
- **PR**: #95
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +246/-47 in 5 files
- **Labels**: none

## Connections
