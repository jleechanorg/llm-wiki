---
title: "Faction Ranking Calculation Tests"
type: source
tags: [python, testing, faction-combat, ranking, fp-calculation, game-mechanics]
source_file: "raw/test_faction_ranking_calculation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying faction ranking calculation functions including territory multiplier, unit contributions, total FP calculation, and edge cases. Tests validate the formula for territory (*5), soldiers (1x), spies (0.5x), elites (3x at level 6), and fortifications (1000 FP each).

## Key Claims
- **Territory Multiplier**: Territory contributes 5 FP per unit (verified by test_calculate_total_fp_territory_multiplier)
- **Total FP Components**: Army (soldiers + spies + elites) + territory + fortifications + citizens + gold + arcana + prestige
- **Ranking Calculation**: calculate_ranking returns rank position and all factions sorted by FP descending
- **Edge Cases**: Handles missing unit types and rank boundary conditions

## Key Quotes
> "Territory FP should be 100 * 5 = 500" — test_calculate_total_fp_territory_multiplier

## Connections
- [[Faction Combat Power Calculation Tests]] — complementary tests for the same calculation logic
- [[Faction Ranking Recompute Tests]] — validates ranking auto-recompute when LLM emits stale FP

## Contradictions
- None detected
