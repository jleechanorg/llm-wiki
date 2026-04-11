---
title: "PR #152: fix(mem0): fix session scanner to find all Claude/Codex sessions"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-152.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Claude sessions were completely missed (29,592 files) — UUID-named JSONL with no `sessions/` in path
- Codex `archived_sessions/` and `sessions_archive/` dirs were missed (7,108 files)
- Scanner now finds **43,120 sessions** (was 9,182)

## Metadata
- **PR**: #152
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +89/-20 in 1 files
- **Labels**: none

## Connections
