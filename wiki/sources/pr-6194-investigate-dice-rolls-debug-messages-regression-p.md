---
title: "PR #6194: investigate: dice rolls & debug messages regression (pre-#6161)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6194.md
sources: []
last_updated: 2026-04-11
---

## Summary
On current main, the game UI does not render **dice roll entries** or **debug messages** (debug_info) even when the user has `debug_mode=true` in their settings. On the mvp-stable production deployment (~Mar 21 2026, commit `02a6e5fb3`), both features work correctly. This is a regression window of approximately 3 weeks.

Critically, **the user reports these symptoms predate PR #6161** (merged Apr 11 as commit `d868fec0c`). That means PR #6161 is NOT the root cause for dice/debug — it IS the root

## Metadata
- **PR**: #6194
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +167/-0 in 1 files
- **Labels**: none

## Connections
