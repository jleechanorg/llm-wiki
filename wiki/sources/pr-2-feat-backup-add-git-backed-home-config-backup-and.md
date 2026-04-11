---
title: "PR #2: feat(backup): add git-backed home config backup and scheduler install"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-/pr-2.md
sources: []
last_updated: 2026-03-07
---

## Summary
This PR turns `user_scope` into a git-backed machine config backup repo for Claude/Codex home configuration.

Compared with `origin/main`, it:
- commits the restore-useful backup snapshot under `backup/Mac/`
- adds automated home backup scripting via `scripts/backup-home.sh`
- adds cross-platform scheduler installation via root `install.sh`
- retargets the legacy conversation-backup installer to the new home-backup script
- adds privacy/hygiene guards so large or sensitive runtime artifacts stay

## Metadata
- **PR**: #2
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +16809/-9 in 104 files
- **Labels**: none

## Connections
