---
title: "PR #309: [agento] feat: slash command web discovery for non-Claude agents"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-309.md
sources: []
last_updated: 2026-03-30
---

## Summary
Non-Claude agents (primarily **Codex**, OpenAI's CLI) cannot natively understand Claude slash commands like `/er`, `/fixpr`, `/simplify`, etc. The current `/claw` dispatch system resolves slash commands from pre-committed local files — if a command hasn't been committed locally, Codex workers cannot discover it.

MiniMax uses Claude internally and may understand slash commands natively. Cursor CLI has its own slash system. Only Codex and similar agents that do NOT natively support slash commands

## Metadata
- **PR**: #309
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +134/-0 in 1 files
- **Labels**: none

## Connections
