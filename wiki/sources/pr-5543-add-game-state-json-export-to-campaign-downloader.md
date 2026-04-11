---
title: "PR #5543: Add game state JSON export to campaign downloader"
type: source
tags: []
date: 2026-02-15
source_file: raw/prs-worldarchitect-ai/pr-5543.md
sources: []
last_updated: 2026-02-15
---

## Summary
- update `scripts/download_campaign.py` to export two files per campaign download:
  - story export in selected format (`txt`/`docx`/`pdf`)
  - game state export as `*_game_state.json`
- align filenames by introducing a shared filename prefix
- improve CLI output to report both saved files and sizes
- add a defensive fallback to basic story formatting when enhanced formatting crashes on malformed legacy `planning_block.choices`

## Metadata
- **PR**: #5543
- **Merged**: 2026-02-15
- **Author**: jleechan2015
- **Stats**: +53/-19 in 1 files
- **Labels**: none

## Connections
