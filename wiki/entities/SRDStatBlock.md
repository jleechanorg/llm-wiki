---
title: "SRD Stat Block"
type: entity
tags: [dnd-srd, data-structure]
sources: [srd-stat-block-mapping-faction-units]
last_updated: 2026-04-08
---

TypedDict defining the structure of a D&D 5.1 SRD creature stat block. Contains fields for name, AC, HP, attack bonus, damage dice, challenge rating, and creature traits.

## Fields
- `name`: Creature name from SRD
- `ac`: Armor Class
- `hp`: Hit Points
- `attack_bonus`: Melee/ranged attack modifier
- `damage_dice`: Damage formula (e.g., "1d6+1")
- `cr`: Challenge Rating (0.125-8.0)
- `traits`: List of special abilities (e.g., sneak_attack, evasion)

## Usage
Used by [[SRDStatBlockMappingFactionUnits]] to resolve faction units into D&D stat blocks for combat simulation.
