---
title: "PR #5955: feat: add /claw command for direct OpenClaw gateway dispatch (no timeout)"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldarchitect-ai/pr-5955.md
sources: []
last_updated: 2026-03-14
---

## Summary
- Adds `/claw` slash command to `.claude/commands/claw.md`
- Dispatches tasks directly to OpenClaw gateway (`http://127.0.0.1:18789/v1/chat/completions`) via `nohup curl &` (fire-and-forget)
- No 30s timeout — long coding tasks (20+ min) run until complete

## Metadata
- **PR**: #5955
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +74/-0 in 1 files
- **Labels**: none

## Connections
