---
title: "PR #19: feat: move SQLite DB from repo root to ~/.worldai_claw/"
type: source
tags: []
date: 2026-02-25
source_file: raw/prs-worldai_claw/pr-19.md
sources: []
last_updated: 2026-02-25
---

## Summary
- Default SQLite path changed from `process.cwd()/worldai_claw.db` to `~/.worldai_claw/worldai_claw.db`
- All worktrees share one database instead of duplicating per cwd
- `SQLITE_DB_PATH` env override unchanged for testing

## Metadata
- **PR**: #19
- **Merged**: 2026-02-25
- **Author**: jleechan2015
- **Stats**: +111/-10 in 5 files
- **Labels**: none

## Connections
