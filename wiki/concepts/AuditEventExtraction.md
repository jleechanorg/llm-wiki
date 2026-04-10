---
title: "Audit Event Extraction"
type: concept
tags: [telemetry, dice-rolling, data-processing]
sources: [action-resolution-dice-roll-extraction-helpers]
last_updated: 2026-04-08
---

## Definition
The process of extracting structured audit events from action_resolution.mechanics.audit_events for dice telemetry and evaluation purposes.

## Extraction Logic
1. Extract audit_events list from mechanics
2. Convert string events to dict format if needed
3. Fall back to extracting from rolls if no audit_events present
4. Compute modifiers and totals from raw roll data

## Event Structure
```python
{
    "source": "code_execution",
    "label": "Attack Roll",
    "notation": "1d20+5",
    "rolls": [15, 5],
    "modifier": 5,
    "total": 20,
    "dc": 15,
    "success": True
}
```

## Related Concepts
- [[DiceRollMechanics]] — source of roll data
- [[DiceTelemetry]] — system consuming audit events
- [[ActionResolution]] — parent structure
