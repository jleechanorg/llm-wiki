---
title: "Territory Multiplier"
type: concept
tags: [game-mechanics, faction-power, calculation]
sources: [faction-ranking-calculation-tests, faction-combat-power-calculation-tests]
last_updated: 2026-04-08
---

The factor by which territory count contributes to Faction Power (FP). Each territory unit adds 5 FP to the total faction power calculation.

## Formula
```
territory_fp = territory_count * 5
```

## Verification
Test `test_calculate_total_fp_territory_multiplier` verifies that 100 territory yields 500 FP (100 * 5).

## Related
- [[Faction Combat Power Calculation Tests]]
- [[Faction Power (FP)]]
