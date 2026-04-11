---
title: "PR #341: [P1] fix: dispatch-task skill — call ao spawn directly, retire dispatch_task.py path"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-341.md
sources: []
last_updated: 2026-03-21
---

## Summary
dispatch_task.py was deleted from mctrl (ao_cli.py is now a tombstone: 'use ao CLI directly'). But the dispatch-task skill still told OpenClaw to run it. Additionally, OpenClaw was using sessions_spawn (internal nested LLM) and ai_orch (old Python runner) instead of ao (agento).

Two bugs this fixes:
1. Worker not auto-submitting — ai_orch pastes prompt but does not press Enter; ao send handles this
2. dispatch_task.py no longer exists — skill was pointing at a deleted module

## Metadata
- **PR**: #341
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +36/-32 in 1 files
- **Labels**: none

## Connections
