---
title: "Equipment Registry"
type: concept
tags: [game-design, items, data-structure]
sources: []
last_updated: 2026-04-08
---

## Summary
A data structure in the game that maps item IDs to full item properties. Allows equipment to be referenced by compact IDs while providing access to full stats like damage, properties, and stat bonuses.

## Key Details
- Items stored in player_character_data.item_registry
- Registry entries include: name, damage, properties, stats (with optional caps like "(Max 19)")
- The extract_equipped_weapons function resolves registry IDs to full weapon data
- Equipment bonuses are capped according to registry specifications

## Related
- [[stats_display]]
- [[Proficiency Bonus]]
