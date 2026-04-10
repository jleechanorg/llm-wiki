---
title: "Arcana Yield"
type: concept
tags: [game-mechanics, magic, resource-management, mana]
sources: [faction-resource-calculation-formulas]
last_updated: 2026-04-08
---

## Definition
Magic resource generation formula based on mana font buildings and territory ratio.

## Formula
```
X = floor(100 × mana_fonts / territory)
Yield = (territory/1000 × X)/100 + mana_fonts × (100 - X)/10
```

## Key Insight
Optimal mana font ratio is **55-55.99%** of territory. Above 56%, diminishing returns kick in and yield decreases.

## Related Concepts
- [[Mana Fonts]] — building type that generates arcana
- [[Territory Management]] — denominator in ratio calculation
- [[Faction Power Rankings System]] — arcana is a factor in faction strength
