---
title: "Gold Calculation"
type: concept
tags: ["economy", "state", "calculation"]
sources: ["llm-first-state-management-plan-pr-2778"]
last_updated: 2026-04-07
---

# Gold Calculation

## Definition
System for correctly tracking character and faction wealth changes in narratives.


## Rules
- **Always calculate**: Previous Gold - Costs + Rewards = New Gold
- **Show calculation before narrative**
- **Faction Mode**: Track BOTH character.gold (personal) AND faction.resources.gold (faction treasury) separately

## Normal Campaign Example
```
Previous character gold: 110gp
Action: Buy equipment (cost: 100gp)
Calculation: 110 - 100 = 10gp
New character gold: 10gp
```

## Faction Campaign Example
```
Previous character gold: 110gp (personal wealth)
Previous faction gold: 500gp (faction treasury)
Action: Build library (cost: 100gp from faction treasury)
Character gold calculation: 110 - 0 = 110gp (unchanged)
Faction gold calculation: 500 - 100 = 400gp
```

## Related Issues
- Scene 18 shows 110gp when should be 10gp (fixed by prompt engineering)
- Dual gold tracking confusion in faction campaigns
