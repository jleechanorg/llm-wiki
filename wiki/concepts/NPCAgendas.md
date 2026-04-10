---
title: "NPC Agendas"
type: concept
tags: [game-mechanic, npc-behavior, progression]
sources: ["time-pressure-game-state"]
last_updated: 2026-04-08
---

## Definition
NPC agendas track the goals, progress, and milestones of non-player characters in the game world. They progress over game time and can be influenced by player actions.

## Structure
```python
{
    "current_goal": "Sell captured merchant to slavers",
    "progress_percentage": 30,
    "next_milestone": {
        "day": 23,
        "hour": 12,
        "description": "Meet with slaver representative",
    },
    "blocking_factors": ["guard patrols", "PC interference"],
    "completed_milestones": ["Captured merchant"],
}
```

## Key Properties
- **progress_percentage**: 0-100 progress toward current goal
- **next_milestone**: Upcoming objective with specific game time
- **blocking_factors**: What could prevent goal completion
- **completed_milestones**: History of achieved objectives

## Related Concepts
- [[TimeSensitiveEvents]] — events often tied to NPC goals
- [[ConsequenceTriggers]] — outcomes when NPCs achieve their goals
