---
title: "Gold Income"
type: concept
tags: [game-mechanics, economy, resource-management, gold]
sources: [faction-resource-calculation-formulas]
last_updated: 2026-04-08
---

## Definition
Resource generation formula for faction wealth in WorldAI Faction Management.

## Income Sources
| Source | Formula | Per Unit |
|--------|---------|----------|
| Tax Revenue | citizens × 0.5 | 0.5gp per citizen |
| Farm Surplus | farms × 100 | 100gp per farm |
| Trade Routes | artisans_guilds × 200 | 200gp per workshop |
| Prosperity Ritual | base × 2 | 2× multiplier |

## Usage
Gold is used for:
- Building construction
- Unit recruitment
- NPC interactions (via [[NPC Relationship Trust System]])

## Related Concepts
- [[Faction Power Rankings System]] — economic strength factor in FP calculation
- [[Prosperity Ritual]] — temporary income doubling buff
