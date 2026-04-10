---
title: "Entity Type Taxonomy"
type: concept
tags: [entities, taxonomy, game-objects]
sources: ["game-state-schema-json"]
last_updated: 2026-04-08
---

## Definition
The six core entity types in WorldArchitect.AI's game model.

## Entity Types
| Type | Code | Description |
|------|------|-------------|
| Player Character | pc | User-controlled character |
| Non-Player Character | npc | DM-controlled character |
| Creature | creature | Monsters, animals, beasts |
| Location | loc | Places, regions, buildings |
| Item | item | Equipment, objects, magic items |
| Faction | faction | Organizations, groups |
| Object | obj | Generic interactive objects |

## Entity ID Format
Entity IDs follow the format: `{type}_{name}_{sequence}` (e.g., `character_theron_001`, `npc_merchant_001`)

## Related Concepts
- [[EntityStatus]] — Entity health/disposition states
- [[Visibility]] — Entity visibility conditions
- [[EntityTrackingSystem]] — Tracking implementation
