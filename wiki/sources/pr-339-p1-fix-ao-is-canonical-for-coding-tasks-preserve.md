---
title: "PR #339: [P1] fix: ao is canonical for coding tasks — preserve+expand task text, ban sessions_spawn"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-339.md
sources: []
last_updated: 2026-03-21
---

## Summary
When OpenClaw dispatches a coding task to a worker, it has two paths: its internal sessions_spawn tool (nested LLM, no worktree) and ao spawn (external CLI, real git worktree + tmux). For orch-han, OpenClaw chose sessions_spawn and silently rewrote the task — dropping /claw and mctrl_test repo instructions. The worker also never auto-submitted (sessions_spawn pastes but does not press Enter).

## Metadata
- **PR**: #339
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +33/-0 in 2 files
- **Labels**: none

## Connections
