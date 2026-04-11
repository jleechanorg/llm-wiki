---
title: "PR #5673: fix(llm_service): guard against dict current_location in _tier_entities"
type: source
tags: []
date: 2026-02-20
source_file: raw/prs-worldarchitect-ai/pr-5673.md
sources: []
last_updated: 2026-02-20
---

## Summary
- Production crash on campaign `uMkxhFVWRyGatnnV3qRj`: `AttributeError: 'dict' object has no attribute 'strip'` in `_tier_entities()` blocked every stream
- `world_data["current_location_name"]` stored as a dict (`{"id": "loc_ashwood_keep_001", "name": "Ashwood Keep"}`) instead of a plain string for some campaigns
- Same dict risk existed for NPC `current_location` fields inside `_tier_entities`

## Metadata
- **PR**: #5673
- **Merged**: 2026-02-20
- **Author**: jleechan2015
- **Stats**: +153/-3 in 2 files
- **Labels**: none

## Connections
