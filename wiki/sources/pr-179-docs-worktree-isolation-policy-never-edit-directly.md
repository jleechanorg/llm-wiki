---
title: "PR #179: docs: worktree isolation policy — never edit ~ directly"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-179.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Establishes rule: all file edits must happen in the worktree, never directly in ~/.openclaw/ or ~/
- Covers all files (SOUL.md, CLAUDE.md, agent-orchestrator.yaml, scripts, etc.)
- ~/.openclaw/ is updated via git pull after PR merges to main
- ~/agent-orchestrator.yaml (outside repo) requires one manual cp after pull

## Metadata
- **PR**: #179
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +27/-0 in 2 files
- **Labels**: none

## Connections
