---
title: "PlanningChoice"
type: concept
tags: [schema, planning-block, canonicalization, choice-contract]
sources: [opaque-choice-ids-resolver-contract-2026-05-15]
last_updated: 2026-05-15
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

## Opaque ID Migration

For PR6906 follow-up work, `id` should be treated as an opaque exact-selection
handle. New semantic meaning belongs in explicit fields such as `intent`,
`execution`, and `ui`, then in selected-choice resolver output. Correction
guards and modal scrubbers should not infer meaning from ID prefixes.
