---
title: "Faction Combat Power Calculation Tests"
type: source
tags: [python, testing, faction-combat, power-calculation, game-mechanics]
source_file: "raw/test_faction_combat_power.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests verifying the faction power calculation formula. Tests validate territory multiplier (should be 5, not 10), soldier FP contribution (1x), spy contribution (0.5x), elite contribution (3x at level 6 with level bonus above 6), and total calculation with fortifications. Also tests edge cases with missing or zero unit types.

## Key Claims
- **Territory Multiplier**: Territory contributes 5 FP per unit (not 10)
- **Soldiers**: 1.0x FP multiplier each
- **Spies**: 0.5x FP multiplier each
- **Elites**: 3.0x FP multiplier at level 6, with level bonus above 6 (1.0 + (level-6)*0.1)
- **Fortifications**: 1000 FP each
- **Total Calculation**: soldiers + spies + elites + territory + fortifications = total FP
- **Edge Cases**: Handles missing unit types and zero values gracefully

## Key Test Cases
```python
# Territory: 100 * 5 = 500 FP
calculate_faction_power(soldiers=0, spies=0, elites=0, territory=100, fortifications=0)

# Total: 100*1.0 + 50*0.5 + 10*3.0 + 200*5 + 2*1000 = 3155 FP
calculate_faction_power(soldiers=100, spies=50, elites=10, elite_avg_level=6, territory=200, fortifications=2)
```

## Connections
- [[Faction Power Calculation]] — the formula being tested
- [[MVP Site]] — contains mvp_site.faction.combat module

## Contradictions
- None identified
