---
title: "Compacted State Reversion"
type: concept
tags: [compaction, json, truncation, budget-allocation, state-management]
sources: []
last_updated: 2026-04-11
---

## Description
When context budget is exceeded, `_compact_game_state` truncates the JSON string. If truncation produces invalid JSON, `llm_service` falls back to the original (non-compacted) state — defeating compaction exactly when it was most needed.

## Symptoms
- Context budget exceeded → compaction attempted
- Truncated JSON is invalid → `json.loads()` fails
- Fallback to original state → no compaction applied
- Input still exceeds budget → request may fail downstream

## Root Cause
`_compact_game_state` truncates at byte level:
```python
compact = json.dumps(state)
if len(compact) > max_chars:
    compact = compact[:max_chars]  # may cut mid-character, mid-token
# llm_service.py:3926
try:
    state = json.loads(compact)
except JSONDecodeError:
    state = original_state  # reverts to full state
```

## Fix
Use structured truncation that preserves JSON validity:
```python
def compact_json_structured(data, max_chars):
    """Truncate by removing lowest-priority keys, not bytes."""
    compact = json.dumps(data)
    if len(compact) <= max_chars:
        return compact
    # Remove keys from lowest priority sections until valid
    ...
    return compact
```

Or: validate after truncation and provide a minimal fallback structure.

## Connections
- [[Compaction]] — context compaction system
- [[Context-Bloat]] — root cause: excessive context
