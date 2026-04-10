---
title: "EquipmentDisplayModule"
type: entity
tags: [module, equipment, ui, mvp-site]
sources: [equipment-display-module-tests]
last_updated: 2026-04-08
---

## Description
Python module in mvp_site that handles equipment display extraction, categorization, and formatting for game UI. Provides functions to detect equipment queries, classify equipment slots, and generate equipment summaries.

## Key Functions
- `is_equipment_query()` - Detect equipment-related queries
- `classify_equipment_query()` - Classify query type (backpack, weapons, equipped, all)
- `_categorize_equipment_slot()` - Categorize equipment slots
- `extract_equipment_display()` - Extract equipment data from game state
- `ensure_equipment_summary_in_narrative()` - Add equipment to narrative output

## Related
- [[EquipmentDisplayModuleTests]]
- [[MVP Site]] - parent project
