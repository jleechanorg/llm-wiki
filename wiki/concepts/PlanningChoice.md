---
title: "PlanningChoice"
type: concept
tags: [schema, planning-block, canonicalization]
sources: []
last_updated: 2026-04-08
---

Canonical schema for planning block choice objects. A list of PlanningChoice objects is the canonical format for `PlanningBlock.choices`.

## Schema
```python
@dataclass
class PlanningChoice:
    id: str           # Unique identifier
    text: str         # Display text
    description: str  # Optional description
    risk_level: str  # safe, low, medium, high
```

## Canonicalization
The `normalize_planning_block_choices` function ensures all choices conform to this schema by converting from dict format and handling edge cases.
