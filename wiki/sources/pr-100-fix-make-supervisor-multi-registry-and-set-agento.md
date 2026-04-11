---
title: "PR #100: fix: make supervisor multi-registry and set agento as default orchestrator lane"
type: source
tags: []
date: 2026-03-11
source_file: raw/prs-worldai_claw/pr-100.md
sources: []
last_updated: 2026-03-11
---

## Summary
- make supervisor reconcile multiple registry files in one loop (including sibling workspace roots sharing the same `.messages` backend)
- remove single-root/cwd coupling that caused mctrl runs to stay `in_progress` when they were dispatched from a different repo root
- update OpenClaw policy docs so orchestrator layers are explicit: `agento` default for change requests, `mctrl` opt-in lane

## Metadata
- **PR**: #100
- **Merged**: 2026-03-11
- **Author**: jleechan2015
- **Stats**: +385/-28 in 10 files
- **Labels**: none

## Connections
