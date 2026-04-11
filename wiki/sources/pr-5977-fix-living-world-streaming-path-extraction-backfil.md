---
title: "PR #5977: fix(living-world): streaming path extraction + backfill for world events"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5977.md
sources: []
last_updated: 2026-03-15
---

## Summary
- Streaming persist path now extracts world_events from state_updates (including custom_campaign_state nesting)
- Normalizes, annotates with turn/scene, and backfills when LLM omits events
- Filters to current scene to prevent cumulative history bleed
- Adds sequence_id and user_scene_number for non-streaming parity

## Metadata
- **PR**: #5977
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +117/-27 in 2 files
- **Labels**: none

## Connections
