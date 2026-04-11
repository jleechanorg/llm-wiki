---
title: "PR #29: feat(novel): FIFO bidirectional chat + parseFifoLines pure function"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-/pr-29.md
sources: []
last_updated: 2026-03-29
---

## Summary
Section E of the design doc describes a FIFO-based bidirectional IPC channel so Claude Code operator sessions can have character-consistent chats with AO worker sessions via named pipes (`~/.blog/inbox/{workerId}`). This PR implements that mechanism and integrates it as the Tier 0 inference backend in `chat_worker`.

## Metadata
- **PR**: #29
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +273/-0 in 3 files
- **Labels**: none

## Connections
