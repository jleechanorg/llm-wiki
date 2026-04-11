---
title: "Stats Display Module Unit Tests"
type: source
tags: [tdd, unit-testing, python, stats, equipment, weapons]
source_file: "raw/stats-display-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the stats_display module covering proficiency bonus calculation, spellcasting ability detection, weapon extraction, equipment bonuses, and stats summary generation. Tests handle edge cases like multi-class characters, equipment registry items, and stat caps.

## Key Claims
- **Proficiency Bonus Coercion**: get_proficiency_bonus safely handles string inputs, invalid values, and high levels by coercing to integers and clamping to D&D bounds (levels 1-20 map to +2 to +6)
- **Spellcasting Ability Detection**: get_spellcasting_ability parses multi-class characters (e.g., "Fighter/Wizard" → int, "Rogue/Paladin" → cha) and recognizes class variants like Blood Hunter and Eldritch Knight
- **Weapon Extraction with Registry Support**: extract_equipped_weapons resolves registry item IDs into full weapon data and distinguishes thrown weapons from ranged/finesse weapons
- **Equipment Bonuses with Caps**: extract_equipment_bonuses respects (Max X) caps from registry items, clamping bonuses appropriately
- **Non-proficient Weapons**: Weapons without proficiency display damage without adding the proficiency bonus

## Connections
- [[stats_display]] — module under test
- [[Proficiency Bonus]] — game mechanic for calculating bonus based on character level
- [[Equipment Registry]] — system for looking up item properties by ID
- [[Multi-classing]] — D&D rule allowing characters to have multiple classes
