---
title: "PR #389: feat(mem0): Claude Code hooks for automatic memory recall + save (dual-write Qdrant + markdown)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-389.md
sources: []
last_updated: 2026-03-24
---

## Summary
The openclaw mem0 Qdrant store accumulates session facts from openclaw agent sessions. Claude Code sessions (jleechan terminal sessions) were not connected to this store — every Claude session started with no memory of prior work.

This PR wires Claude Code into the shared mem0 memory store via two hooks registered in `.claude/hooks/`.

## Metadata
- **PR**: #389
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +317/-0 in 4 files
- **Labels**: none

## Connections
