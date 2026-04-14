---
title: "mvp_site equipment_display"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/equipment_display.py
---

## Summary
Equipment display and inventory formatting utilities providing deterministic (non-LLM) functions for extracting, categorizing, and formatting equipment data from game state. Detects equipment queries and builds equipment summaries for UI display.

## Key Claims
- is_equipment_query() detects if user is asking about equipment/inventory via keywords
- classify_equipment_query() classifies scope: "backpack", "weapons", "equipped", "all"
- extract_equipment_display() extracts equipment from game_state with categorization
- ensure_equipment_summary_in_narrative() appends equipment summary to narrative text
- MAX_BACKPACK_ITEMS_DISPLAY = 3 items in summary
- KNOWN_EQUIPMENT_SLOTS from schema utilities for canonical slot names

## Connections
- [[GameState]] — equipment extraction from game state
- [[CombatSystem]] — weapon slot categorization
