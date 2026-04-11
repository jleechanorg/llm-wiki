---
title: "Faction Power Rankings System"
type: source
tags: [factions, ranking, game-mechanics, power-calculation, worldarchitect]
source_file: "raw/faction_rankings.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Implements the faction power (FP) calculation system for WorldAI Faction Management, including formulas for total FP, army FP, and AI faction behavior tracking. Supports 200 dynamically generated AI factions with unique behaviors and difficulty levels.

## Key Claims
- **Army FP Formula** — Soldiers: 1.0x, Spies: 0.5x (combat penalty), Elites: 3.0x with level bonus (+10% per level above 6)
- **Total FP Components** — Army + Territory (5 FP/acre) + Fortifications (1000 FP) + Citizens (0.1) + Gold (0.001) + Arcana (0.01) + Prestige (100)
- **200 AI Factions** — Dynamically generated with 14 unique behavior types (defensive, isolationist, trader, raider, expansionist, etc.)
- **Deterministic Generation** — Uses seeded generation for consistent faction lists across sessions

## Key Formulas
| Component | Formula | Multiplier |
|-----------|---------|------------|
| Soldiers FP | soldiers × 1.0 | 1.0 |
| Spies FP | spies × 0.5 | 0.5 |
| Elites FP | elites × 3.0 × level_bonus | 3.0+ |
| Territory FP | territory × 5 | 5 |
| Fortifications FP | fortifications × 1000 | 1000 |
| Citizens FP | citizens × 0.1 | 0.1 |
| Gold FP | gold_pieces × 0.001 | 0.001 |
| Arcana FP | arcana × 0.01 | 0.01 |
| Prestige FP | prestige × 100 | 100 |

## AI Faction Behaviors
- **defensive**: Focuses on fortifications and territory defense
- **isolationist**: Avoids conflict, builds internally
- **trader**: Prioritizes gold income and diplomatic relations
- **raider**: Opportunistic attacks on weaker neighbors
- **expansionist**: Constantly seeks to grow territory
- **balanced**: Well-rounded approach to all aspects
- **aggressive**: Prioritizes military buildup and attacks
- **arcane**: Focuses on arcana and magical research
- **diplomatic**: Seeks alliances and avoids direct conflict
- **shadowy**: Heavy spy network, sabotage operations
- **nature**: Defensive, prefers guerilla tactics
- **imperial**: Structured expansion, tribute demands
- **mysterious**: Unpredictable actions, unknown motives
- **dominating**: Seeks absolute regional control
- **crusading**: Attacks based on ideological motives

## Connections
- [[Prompts Directory]] — Prompts reference faction mechanics
- [[Memory Management Utilities for Core Memories]] — Memory system may reference faction state
