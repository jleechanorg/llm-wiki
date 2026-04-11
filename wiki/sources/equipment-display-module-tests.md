---
title: "Equipment Display Module Tests"
type: source
tags: [python, testing, equipment-display, inventory-management, ui-components]
source_file: "raw/test_equipment_display.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the equipment_display module. Tests validate equipment query detection, equipment slot categorization, backpack item classification, and equipment summary extraction with formatting functions.

## Key Claims
- **is_equipment_query**: Detects equipment-related keywords (equipment, inventory, gear, backpack, weapons) case-insensitively
- **classify_equipment_query**: Classifies queries into categories: backpack, weapons, equipped, all
- **_categorize_equipment_slot**: Categorizes equipment slots into Head, Armor, Boots, Weapons, Off-Hand, Backpack, Rings, Other
- **_classify_backpack_item**: Classifies backpack items by importance and type
- **_get_backpack_importance**: Determines item importance for display prioritization
- **_limit_backpack_for_display**: Limits backpack items for display
- **extract_equipment_display**: Extracts equipment display data from game state
- **ensure_equipment_summary_in_narrative**: Ensures equipment summary is included in narrative output

## Key Test Cases
- `test_equipment_keyword`, `test_inventory_keyword`, `test_gear_keyword` - keyword detection
- `test_backpack_query`, `test_weapons_query`, `test_equipped_query` - query classification
- `test_head_slots`, `test_armor_slots`, `test_weapon_slots` - slot categorization
- Various classification and importance tests for backpack items

## Connections
- [[EquipmentDisplayModule]] — the module being tested
- [[InventoryManagement]] — related concept
- [[EquipmentSlotCategorization]] — related concept
