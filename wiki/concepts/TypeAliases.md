---
title: "Type Aliases"
type: concept
tags: [python, typing]
sources: [python-typing-guide]
last_updated: 2026-04-08
---

Type aliases in WorldArchitect.AI simplify complex types: UserId = str, CampaignId = str, EntityId = str, and JsonValue/JsonDict for JSON-compatible types.

## Defined in custom_types.py
```python
UserId = str
CampaignId = str
EntityId = str
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]
JsonDict = Dict[str, JsonValue]
```

## Related
- [[PythonTypingGuide]] — full guide
- [[TypedDict]] — dictionary typing
- [[TypeHints]] — base typing concept
