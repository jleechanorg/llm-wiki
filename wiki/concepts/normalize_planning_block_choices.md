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

## Critical: LLM Inline Overrides Must Name Exact IDs

When requiring specific `planning_block.choices` entries via an LLM inline override (e.g. in `agents.py`), the override must state the literal choice id verbatim:

**Anti-pattern:** `"expose a change choice for spell preparation"` → model ignores or omits it  
**Correct:** `"MANDATORY: include choice with id \`level_up_change_prepared_spells\`"` → model complies

Source: [LevelUpAgent Inline Override Must Name Exact IDs](../sources/levelup-inline-override-exact-ids-2026-05-24.md) (2026-05-24, rev-vcm7y)
