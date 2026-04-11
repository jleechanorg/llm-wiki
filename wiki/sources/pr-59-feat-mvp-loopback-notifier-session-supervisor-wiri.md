---
title: "PR #59: feat: MVP loopback notifier + session supervisor wiring"
type: source
tags: []
date: 2026-03-08
source_file: raw/prs-worldai_claw/pr-59.md
sources: []
last_updated: 2026-03-08
---

## Summary
- remove in-process TaskPoller startup from Mission Control backend path; keep heartbeat mirror optional via board config
- add persisted bead<->session registry (`session_registry.py`) with atomic updates
- add OpenClaw loopback notifier (`openclaw_notifier.py`) with MCP-mail primary + JSONL fallback/drain
- wire supervisor reconciliation to transition missing sessions to `needs_human` and emit `task_needs_human`
- add MVP docs/audit docs and restore missing webhook parser/event exports require

## Metadata
- **PR**: #59
- **Merged**: 2026-03-08
- **Author**: jleechan2015
- **Stats**: +4601/-878 in 72 files
- **Labels**: none

## Connections
