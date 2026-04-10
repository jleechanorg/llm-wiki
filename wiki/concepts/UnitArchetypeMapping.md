---
title: "Unit Archetype Mapping"
type: concept
tags: [game-design, abstraction, faction-system]
sources: [srd-stat-block-mapping-faction-units]
last_updated: 2026-04-08
---

System for resolving diverse, genre-specific unit labels into a canonical set of D&D 5.1 SRD creature archetypes. Enables faction simulation to work across any genre (fantasy, modern, sci-fi) while maintaining consistent mechanical depth.

## Mapping Hierarchy
1. **Direct Match**: Exact key in `UNIT_TO_SRD_MAP`
2. **Alias Lookup**: Check `UNIT_ARCHETYPE_ALIASES` for genre-neutral synonyms
3. **Keyword Matching**: Substring search in `UNIT_KEYWORD_MAP`

## Canonical Archetypes
| Archetype | SRD Creature | CR | Use Case |
|-----------|--------------|-----|----------|
| soldier | Guard | 0.125 | Basic infantry |
| veteran | Veteran | 3.0 | Elite soldiers |
| scout | Scout | 0.5 | Recon units |
| spy | Spy | 1.0 | Infiltration |
| assassin | Assassin | 8.0 | Covert ops |
| elite_6 | Knight | 3.0 | Champions |
| elite_10 | Gladiator | 5.0 | Warlords |

## Example Resolution
```
"marine" → alias "soldier" → map to "guard"
"sniper" → keyword match → map to "assassin"
```
