---
title: "PR #216: feat: backfill-memory-md includes Claude Code auto-memory files"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-216.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Extends `backfill-memory-md-only.mjs` to also scan `~/.claude/projects/*/memory/*.md`
- Product info files written via Claude Code auto-memory (e.g. `project_worldarchitect_ai.md`, `project_worldai_claw.md`, `project_jleechanclaw_goals.md`) now get ingested into mem0/Qdrant when the backfill script runs

## Metadata
- **PR**: #216
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +10/-0 in 1 files
- **Labels**: none

## Connections
