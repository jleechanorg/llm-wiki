---
title: "PR #150: fix(tmux): adaptive delay + Enter retry for long messages (bd-qhf)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-150.md
sources: []
last_updated: 2026-03-24
---

## Summary
Implements upstream ComposioHQ PR #541's fix for issue #373: long tmux paste messages (>200 chars) frequently had their trailing Enter keystroke swallowed because a fixed 1000ms delay was insufficient for large messages.

### What changed

**packages/core/src/tmux.ts**:
- Extract `isLongMessage` check to a named const (DRY)
- Replace inline `new Promise(setTimeout)` with injectable `sleep()` helper wrapping `node:timers/promises`
- **Adaptive delay**: scales with message length — `1000ms + 200ms

## Metadata
- **PR**: #150
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +204/-45 in 2 files
- **Labels**: none

## Connections
