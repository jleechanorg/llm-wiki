---
title: "PR #55: fix: restore files mass-deleted by 7d5b9e1efd + gitignore .openclaw-backups/"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-55.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Restores ~31k files deleted by commit `7d5b9e1efd` which accidentally wiped `scripts/`, `openclaw/`, `openclaw-config/`, `.github/`, and all root-level files
- Carries forward the correct intent from that commit: add `.openclaw-backups/` and `.beads/interactions.jsonl` to `.gitignore`

## Metadata
- **PR**: #55
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +40984/-973 in 1742 files
- **Labels**: none

## Connections
