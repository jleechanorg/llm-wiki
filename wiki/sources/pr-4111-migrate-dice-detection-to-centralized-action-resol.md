---
title: "PR #4111: Migrate dice detection to centralized action_resolution location"
type: source
tags: []
date: 2026-01-30
source_file: raw/prs-worldarchitect-ai/pr-4111.md
sources: []
last_updated: 2026-01-30
---

## Summary
This PR centralizes dice **authoring** into `action_resolution.mechanics.rolls/audit_events`. Legacy `dice_rolls` / `dice_audit_events` fields are now **server-derived** only (no LLM population, no legacy backfill).

## Metadata
- **PR**: #4111
- **Merged**: 2026-01-30
- **Author**: jleechan2015
- **Stats**: +1826/-660 in 30 files
- **Labels**: none

## Connections
