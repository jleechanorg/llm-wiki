---
title: "PR #155: [agento] fix(lifecycle): skip reactions on dead agents (bd-5o1)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-155.md
sources: []
last_updated: 2026-03-25
---

## Summary
When a tmux session is killed manually, the AO session metadata persists. The lifecycle-worker keeps polling, detects PR state changes (e.g. CHANGES_REQUESTED), and fires reactions to a dead session.

## Metadata
- **PR**: #155
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +422/-36 in 5 files
- **Labels**: none

## Connections
