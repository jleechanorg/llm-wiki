---
title: "normalize_planning_block_choices"
type: concept
tags: [function, normalization, planning-block, conversion]
sources: []
last_updated: 2026-04-08
---
---

## Description
Helper function that canonicalizes `PlanningBlock.choices` from dict format to `list[PlanningChoice]`.

## Function Signature
```python
def normalize_planning_block_choices(planning_block: dict | str) -> dict
```

## Behavior
- Accepts dict with `choices` as dict or list
- Accepts JSON string (auto-parsed)
- Returns dict with `choices` as list
- Auto-generates IDs from dict keys when converting
- Adds deterministic suffixes for duplicate IDs

## Examples
```python
# Dict input → list output
{"choices": {"attack": {...}}} → {"choices": [{"id": "attack", ...}]}

# Duplicate IDs
after normalization: [{"id": "attack"}, {"id": "attack_1"}, {"id": "attack_2"}]
```

## Connections
- [[PlanningBlock]] — schema being normalized
- [[PlanningChoice]] — target format
- [[NarrativeResponse]] — calls this function during validation
