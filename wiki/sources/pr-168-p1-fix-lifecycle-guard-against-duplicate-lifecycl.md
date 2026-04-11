---
title: "PR #168: [P1] fix(lifecycle): guard against duplicate lifecycle-workers per project (orch-886k)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-168.md
sources: []
last_updated: 2026-03-25
---

## Summary
`ps aux` shows 2x `lifecycle-worker` processes for `jleechanclaw` and 2x for `agent-orchestrator`. Duplicate workers send contradictory nudges to the same session causing agents to confirm green and stop instead of re-engaging.

Root cause: Two concurrent `lifecycle-worker` processes (e.g. launchd `KeepAlive` restart racing with `ao start`) can both pass the PID-file status check before either records its PID -- a classic TOCTOU race. Additionally, `ensureLifecycleWorker` had no way to detect a

## Metadata
- **PR**: #168
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +402/-10 in 3 files
- **Labels**: none

## Connections
