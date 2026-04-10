---
title: "Equipment Slot System"
type: concept
tags: [equipment, dnd, game-mechanics]
sources: [equipment-display-inventory-formatting-utilities]
last_updated: 2026-04-08
---

## Definition
The equipment slot system categorizes items in a character's inventory by their physical location and function: backpack (carried items), main hand, off hand, and equipped armor. Used for filtering what to display in equipment queries.

## Canonical Slots
- `weapon` / `main hand` / `main_hand` — primary weapons
- `off hand` / `off_hand` — shields, foci, torches
- `backpack` — stored items
- `weapon_secondary` — secondary weapons

## Query Classification
| Query Type | Displayed Slots |
|------------|---------------|
| backpack   | backpack only |
| weapons   | weapon slots |
| equipped  | all except backpack |
| all       | everything |
