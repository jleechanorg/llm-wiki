---
title: "Equipment Display and Inventory Formatting Utilities"
type: source
tags: [python, equipment, inventory, game-state, ui-display]
source_file: "raw/equipment-display-inventory-formatting.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing deterministic functions for extracting, categorizing, and formatting equipment data from game state for UI display. Handles equipment queries with classification into scopes (backpack, weapons, equipped, all) and builds equipment summaries for narrative integration.

## Key Claims
- **Equipment Query Detection**: `is_equipment_query` identifies user intents asking about equipment/inventory/gear
- **Scope Classification**: `classify_equipment_query` returns backpack, weapons, equipped, or all
- **Equipment Filtering**: `_filter_equipment_for_summary` filters by slot with deduplication by name+stats
- **Narrative Integration**: `ensure_equipment_summary_in_narrative` appends equipment summaries to generated narratives
- **Dice Pattern Recognition**: Regex for standard D&D dice notation (2d6+1, 1d8-2)

## Key Functions

### is_equipment_query(user_input: str) -> bool
Detects if user is asking about equipment/inventory using keyword matching against EQUIPMENT_QUERY_KEYWORDS list.

### classify_equipment_query(user_input: str) -> str
Classifies query scope: "backpack", "weapons", "equipped", or "all" based on keyword detection.

### _filter_equipment_for_summary(equipment_display: list, query_type: str) -> list
Filters equipment_display entries by slot type with weapon/off-hand/shield detection for appropriate display context.

## Connections
- Related to [[Entity Tracking System]] for entity presence validation in narratives
- Used with [[Combat System Protocol]] for equipment display during combat
- Supports [[Defensive Numeric Converter]] for stat parsing
