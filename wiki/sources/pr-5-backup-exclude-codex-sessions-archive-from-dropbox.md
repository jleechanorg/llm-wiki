---
title: "PR #5: backup: exclude codex sessions_archive from Dropbox sync"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-/pr-5.md
sources: []
last_updated: 2026-03-09
---

## Summary
- exclude `~/.codex/sessions/sessions_archive/` from the Dropbox sync path in `scripts/backup-home.sh`
- keep exclusion configurable via `CODEX_SESSIONS_EXCLUDE_PATTERNS` (default `sessions_archive/`)
- add regression test to ensure archived sessions are not copied while active sessions are still copied

## Metadata
- **PR**: #5
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +30/-1 in 13 files
- **Labels**: none

## Connections
