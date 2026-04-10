---
title: "normalize_planning_block_choices"
type: concept
tags: [function, normalization, planning-block]
sources: []
last_updated: 2026-04-08
---

Function in `campaign_upgrade` module that normalizes `PlanningBlock.choices` to canonical list format.

## Behavior
- **List input**: Passes through with IDs preserved
- **Dict input**: Converts to list format, using dict keys as choice IDs
- **Empty IDs**: Falls back to slugified text from the "text" field
- **Duplicate IDs**: Appends deterministic suffixes (_1, _2, etc.)
- **None/empty input**: Returns empty choices list

## Usage
```python
result = campaign_upgrade.normalize_planning_block_choices(planning_block)
```
