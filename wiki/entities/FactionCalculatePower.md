---
title: "FactionCalculatePower"
type: entity
tags: [tool, faction-combat, power-calculation]
sources: [faction-ranking-recompute-tests, faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

Faction combat tool that calculates the player's faction power based on units, territory, and buildings. Must be executed before [[FactionCalculateRanking]] to ensure accurate ranking values.

## Power Formula
- Soldiers: 1.0x FP multiplier each
- Spies: 0.5x FP multiplier each
- Elites: 3.0x FP multiplier at level 6, with level bonus above 6
- Territory: 5 FP per unit (not 10)
- Fortifications: 1000 FP each

## Auto-Invocation
When LLM emits ranking without power, the system auto-invokes power calculation and attaches ranking with correct FP values.
