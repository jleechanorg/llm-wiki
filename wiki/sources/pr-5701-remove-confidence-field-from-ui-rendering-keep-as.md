---
title: "PR #5701: Remove confidence field from UI rendering, keep as mechanics-only"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldarchitect-ai/pr-5701.md
sources: []
last_updated: 2026-02-22
---

## Summary
Remove the `confidence` field from player-facing UI rendering across the codebase. The `confidence` field is now strictly mechanics-only (used for DC modifier calculations) and should never be displayed to players. Instead, confidence is expressed through the language and framing of pros/cons.

## Metadata
- **PR**: #5701
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +35/-40 in 4 files
- **Labels**: none

## Connections
