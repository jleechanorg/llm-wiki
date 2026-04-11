---
title: "PR #6094: [agento] fix(data): wrap game state update in Firestore transaction with READ (P0)"
type: source
tags: []
date: 2026-04-05
source_file: raw/prs-worldarchitect-ai/pr-6094.md
sources: []
last_updated: 2026-04-05
---

## Summary
`update_campaign_game_state` (firestore_service.py:2983-3087) had a write-only Firestore transaction with no READ inside. Concurrent writes both succeeded (last-write-wins with no conflict detection) — silent data loss on inventory, HP, quest progress, etc.

## Metadata
- **PR**: #6094
- **Merged**: 2026-04-05
- **Author**: jleechan2015
- **Stats**: +1102/-168 in 12 files
- **Labels**: none

## Connections
