---
title: "Pydantic Model Serialization"
type: concept
tags: [pydantic, serialization, datetime, type-conversion]
sources: ["llm-response-gemini-api-wrapper.md"]
last_updated: 2026-04-08
---

## Definition
Converting Pydantic models to dictionaries or JSON with automatic handling of complex types like datetime, UUID, and enumerations.

## Pattern
```python
# Recommended approach
serialized = model.model_dump(mode="json")

# Fallback for older Pydantic versions
serialized = model.dict()

# Custom serializer for non-standard types
serialized = json_default_serializer(obj)
```

## Key Differences from `dict()`
- `mode="json"` automatically serializes datetime to ISO format strings
- Converts enumerations to string values
- Handles nested models recursively
- Preserves type information for complex structures

## Related Concepts
- [[JSON Serialization]]
- [[NarrativeResponse]]
