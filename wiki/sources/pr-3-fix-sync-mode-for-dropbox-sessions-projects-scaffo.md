---
title: "PR #3: fix: sync mode for Dropbox sessions/projects + scaffold dev scripts"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-/pr-3.md
sources: []
last_updated: 2026-03-07
---

## Summary
- **Bug fix**: `scripts/backup-home.sh` — conversation session/project directories (`sessions/`, `archived_sessions/`, `projects/`) were using additive rsync mode (`--ignore-existing`), so files rewritten in-place were silently skipped on subsequent backup runs. Changed all Dropbox-only session entries to `sync_mode=sync`.
- **TDD regression test**: `test_sessions_updated_in_place_are_recopied_on_second_run` — real rsync round-trip that writes a file, modifies it, runs backup again, and asserts

## Metadata
- **PR**: #3
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +6945/-5 in 29 files
- **Labels**: none

## Connections
