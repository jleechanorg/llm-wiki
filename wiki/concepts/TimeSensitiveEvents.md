---
title: "Time-Sensitive Events"
type: concept
tags: [game-mechanic, time-management, deadline-tracking]
sources: ["time-pressure-game-state"]
last_updated: 2026-04-08
---

## Definition
Time-sensitive events are events in the game that have deadlines — specific points in game time by which the player must complete an objective. Missing a deadline triggers negative consequences.

## Structure
```python
{
    "description": "Rescue kidnapped merchant from bandits",
    "deadline": {
        "year": 1492,
        "month": "Ches",
        "day": 25,
        "hour": 18,
        "minute": 0,
    },
    "consequences": "Merchant will be sold to slavers",
    "urgency_level": "high",  # or "critical"
    "warnings_given": 0,
    "related_npcs": ["Elara (Merchant)", "Garrick (Bandit Leader)"],
    "status": "active",
}
```

## Urgency Levels
- **high**: Important but not critical (e.g., 4 days until deadline)
- **critical**: Immediate threat (e.g., deadline already passed)

## Related Concepts
- [[NPCAgendas]] — related NPC decision-making that affects event outcomes
- [[WarningGeneration]] — system for alerting players to approaching deadlines
