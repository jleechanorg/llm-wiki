---
title: "Citizen Growth"
type: concept
tags: [game-mechanics, population, resource-management]
sources: [faction-resource-calculation-formulas]
last_updated: 2026-04-08
---

## Definition
Mechanic for calculating population growth in WorldAI Faction Management.

## Formula
```
Growth = 50 + int(0.015 × current_citizens)
```

## Capacity Effects
- **0-90% capacity**: Full growth rate
- **90-100% capacity**: Tapered growth (linear reduction)
- **Over 100%**: Negative growth (10% of excess citizens leave)

## Related Concepts
- [[Faction Power Rankings System]] — faction strength depends on citizen count
- [[Territory Management]] — max citizens = territory × 50
