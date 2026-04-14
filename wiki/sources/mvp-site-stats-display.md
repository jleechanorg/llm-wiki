---
title: "mvp_site stats_display"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/stats_display.py
---

## Summary
Shared stats and spells display utilities for API and CLI tools. Provides SPELLCASTING_ABILITY_MAP for D&D 5e classes and calc_modifier() for ability score to modifier conversion.

## Key Claims
- SPELLCASTING_ABILITY_MAP: wizard/bladesinger→INT, cleric/druid/ranger→WIS, bard/sorcerer/warlock/paladin→CHA
- calc_modifier() uses D&D 5e formula: (score - 10) // 2
- Used by both GET /api/campaigns/{id}/stats and scripts/fetch_campaign_gamestate.py

## Connections
- [[GameState]] — character stats display
