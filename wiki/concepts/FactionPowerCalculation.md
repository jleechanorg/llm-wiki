---
title: "Faction Power Calculation"
type: concept
tags: [game-mechanics, combat, power-formula]
sources: [faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

The formula for calculating a faction's combat power (FP) in the game. Used to determine relative faction strength for battle resolution and territory control mechanics.

## Formula
```
Total FP = (soldiers * 1.0) + (spies * 0.5) + (elites * 3.0 * level_bonus) + (territory * 5) + (fortifications * 1000)
```

Where `level_bonus = 1.0 + max(0, elite_avg_level - 6) * 0.1`

## Unit Values
| Unit Type | FP Multiplier | Base Contribution |
|----------|-------------|----------------|
| Soldier | 1.0x | 1 FP each |
| Spy | 0.5x | 0.5 FP each |
| Elite | 3.0x + level bonus | 3+ FP each |
| Territory | 5 | 5 FP per unit |
| Fortification | 1000 | 1000 FP each |

## Usage
Used in faction combat resolution to determine battle outcomes based on relative FP between opposing factions.

## Related Tests
- [[Faction Combat Power Calculation Tests]]
