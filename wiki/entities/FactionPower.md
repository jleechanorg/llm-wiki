---
title: "Faction Power (FP)"
type: entity
tags: [game-mechanic, faction, combat]
sources: [faction-ranking-calculation-tests, faction-ranking-recompute-tests, faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

A numeric value representing a faction's military and economic strength. Used to determine faction rankings and combat capabilities.

## Calculation Formula
```
total_fp = (soldiers * 1) + (spies * 0.5) + (elites * 3 * level_bonus) + (territory * 5) + (fortifications * 1000) + (citizens * 0.1) + (gold_pieces * 0.001) + (arcana * 0.01) + (prestige * 100)
```

## Usage
- Determines faction ranking position
- Used in combat calculations
- Triggers ranking recalculation on staleness detection

## Related
- [[Faction Combat Power Calculation Tests]]
- [[Faction Ranking Recompute Tests]]
