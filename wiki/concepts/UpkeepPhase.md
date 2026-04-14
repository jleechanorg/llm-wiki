---
title: "UpkeepPhase"
type: concept
tags: [faction-management, economy, unit-costs, worldarchitect-ai]
sources: [mvp-site-upkeep]
last_updated: 2026-04-14
---

## Summary

The recurring cost calculation phase for military units in WorldAI Faction Management. Unit upkeep is computed weekly using D&D 5e hireling wage standards, with tiered rates by unit type. UpkeepPhase deduction occurs during world time advancement and funds the FactionMinigame economic balance.

## Key Claims

### Unit Cost Formula
```
upkeep = soldiers * 0.5gp + spies * 1gp + elites * 5gp per week
```

### Unit Tier Rates
| Unit Type | Cost (gp/week) |
|-----------|---------------|
| Soldier | 0.5 |
| Spy | 1.0 |
| Elite | 5.0 |

### Integration Points
- Applied during world time advancement (time moves forward)
- Triggers faction treasury deduction
- Triggers [[FactionMinigame]] economic balancing

## Connections

- [[FactionMinigame]] — broader faction economic system
- [[mvp-site-upkeep]] — Python implementation of upkeep calculation
- [[TurnResolution]] — time advancement triggers upkeep phase