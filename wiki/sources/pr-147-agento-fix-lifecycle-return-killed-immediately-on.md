---
title: "PR #147: [agento] fix(lifecycle): return killed immediately on dead runtime — bd-5o1"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-147.md
sources: []
last_updated: 2026-03-24
---

## Summary
When a tmux session is killed manually, the AO session metadata persists in the filesystem. The lifecycle-worker keeps polling it, detecting PR state changes (e.g. CHANGES_REQUESTED), and firing reactions (`ao send`) to the dead session + notifying OpenClaw.

## Metadata
- **PR**: #147
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +5/-5 in 1 files
- **Labels**: none

## Connections
