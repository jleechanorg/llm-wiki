---
title: "Timestamp Tracking"
type: concept
tags: ["time", "narrative", "state"]
sources: ["llm-first-state-management-plan-pr-2778"]
last_updated: 2026-04-07
---

# Timestamp Tracking

## Definition
System for maintaining logical time progression in AI-generated narratives.

## Rules
- Small actions (build, recruit): +5-15 minutes
- Combat actions: +30-60 minutes
- End turn: +7 days (advance to next week)
- **NEVER go backwards in time**
- If previous was `08:05`, next must be `>= 08:05`

## Example
```
Previous timestamp: 1492 DR, Alturiak 1, 08:05
Current action: Build library (takes ~10 minutes)
New timestamp: 1492 DR, Alturiak 1, 08:15
```

## Related Issues
- Scene 14→15 jumps 08:05→10:45 (fixed by prompt engineering)
- Scene 20→21 reverses 11:15→10:45 (fixed by prompt engineering)
