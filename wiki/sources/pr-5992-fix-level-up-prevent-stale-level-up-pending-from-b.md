---
title: "PR #5992: fix(level-up): prevent stale level_up_pending from blocking planning block"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldarchitect-ai/pr-5992.md
sources: []
last_updated: 2026-03-31
---

## Summary
- **Bug**: `level_up_pending=True` in `custom_campaign_state` caused \"LEVEL UP AVAILABLE!\" to persist in UI, but planning block showed only narrative choices (no level-up option)
- **Root cause**: Three-layer failure — stale `needed_for_next_level` field (64000 instead of 85000), conflicting LLM prompt trigger, and stale flag never written back to Firestore
- **Investigated via**: Direct Firestore query on campaign `b9LPKcLHEwvG4FGsQDpu` (Ramsay V1, seq=343)

## Metadata
- **PR**: #5992
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +688/-78 in 7 files
- **Labels**: none

## Connections
