---
title: "FilterUnknownEntities"
type: concept
tags: [entity-utils, filtering, case-insensitive]
sources: ["entity-utility-functions-tests"]
last_updated: 2026-04-08
---

A utility function that removes "Unknown" entities from a list while preserving order. Used in the entity tracking pipeline to clean entity lists before processing.

## Function Signature
```python
def filter_unknown_entities(entities: list[str]) -> list[str]
```

## Behavior
- Removes any variant of "Unknown" regardless of case (Unknown, unknown, UNKNOWN, etc.)
- Preserves the original ordering of remaining entities
- Returns empty list if input is empty or all entities are unknown
- Does not modify the original list (returns new list)

## Related
- [[IsUnknownEntity]] - predicate function for detecting unknown entities
- [[EntityTracking]] - uses these utilities in the entity filtering pipeline
