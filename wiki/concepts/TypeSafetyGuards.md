---
title: "Type Safety Guards"
type: concept
tags: [defensive-programming, validation, python, testing]
sources: [story-context-tests-consolidated]
last_updated: 2026-04-08
---

## Definition
Defensive programming pattern that adds explicit type checking and validation guards to prevent crashes from malformed input data. Particularly important when handling data from external sources like Firestore that may contain unexpected types.

## Key Patterns
- **isinstance() checks**: Verify input is expected type before accessing attributes
- **get() with defaults**: Use dict.get(key, default) instead of direct key access
- **Early returns**: Exit early when validation fails to prevent further processing
- **Graceful degradation**: Skip invalid entries instead of crashing entire operation

## Example
```python
# Before (crashes on non-dict):
for entry in story_context:
    text = entry.get("text", "")  # AttributeError on string entry

# After (type-safe):
for entry in story_context:
    if not isinstance(entry, dict):
        continue  # Skip invalid entries
    text = entry.get("text", "")
```

## Related Concepts
- [[FirestoreDataHandling]] — handling NoSQL document storage
- [[ContextCompaction]] — budget allocation for LLM context
- [[DefensiveProgramming]] — programming philosophy
