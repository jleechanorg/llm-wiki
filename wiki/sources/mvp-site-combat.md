---
title: "mvp_site — Combat Formulas"
type: source
tags: [worldarchitect-ai, combat, faction-power, damage-calculation, position-multipliers, school-counters]
date: 2026-04-14
source_file: raw/mvp_site_all/combat.py
---

## Summary

Implements exact reverse-engineered formulas for the WorldAI Faction Management combat system: Faction Power (FP) calculation, damage calculation with position multipliers, and school counter bonuses. Replaces heuristic approximations with precise mathematical models.

## Key Claims

### Position Multipliers
| Position | Multiplier |
|----------|-----------|
| ranged | 1.0x (base) |
| melee | 1.5x |
| flying | 2.25x |

### Faction Power (FP) Calculation
- Based on unit composition: soldiers, spies, elites, fortifications, territory, citizens, gold, arcana, prestige
- FP is the core metric for [[rankings]] — all 200 AI factions ranked by total FP

### Damage Calculation
- Input: attacker and defender UnitStats (TypedDict with count, attack, defense, fp_mult, avg_level)
- Formula applies position multipliers first, then school counter bonuses
- Output: damage dealt per combat round

### School Counter System
- Units have "schools" (likely spell/strategy types) that create rock-paper-scissors counter relationships
- Counter bonus applied after position multiplier in damage formula

## Connections

- [[rankings]] — Faction Power drives rankings
- [[mvp-site-ai-factions]] — 200 AI factions that engage in combat
- [[mvp-site-battle-sim]] — D&D 5.1 SRD battle simulation (different system)
- [[DiceAuthenticity]] — combat rolls use dice.py with DICE_SEED for determinism
- [[ArmyFactionPower]] — same concept from campaign-side implementation
