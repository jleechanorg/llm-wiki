---
title: "Dice Roll Mechanics"
type: concept
tags: [dice-rolling, game-mechanics, formatting]
sources: [action-resolution-dice-roll-extraction-helpers]
last_updated: 2026-04-08
---

## Definition
The mechanics sub-structure within action_resolution that contains dice roll data including notation, results, totals, difficulty classes, and purposes.

## Roll Object Format
```python
{
    "notation": "1d20+5",
    "result": 15,
    "total": 20,
    "purpose": "Attack Roll",
    "dc": 15,
    "success": True
}
```

## Display Formatting
- Basic: "notation = total (purpose)"
- With DC: "notation = total vs DC {dc} - Success/Failure (purpose)"

## Related Concepts
- [[ActionResolution]] — parent data structure
- [[DifficultyClass]] — DC tracking
- [[DiceAuditEvents]] — telemetry extraction
