---
title: "PR #186: [antig] Fix Issue #80: Faction cooldown timing"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-186.md
sources: []
last_updated: 2026-04-03
---

## Summary
GitHub issue #80 reported that the faction simulation cooldown was being consumed even when `processInPlayTriggers` encountered an error, because the cooldown timestamp was being set before the simulation logic was awaited.

## Metadata
- **PR**: #186
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +103/-1 in 2 files
- **Labels**: none

## Connections
