---
title: "TypedDict"
type: concept
tags: [python, typing, dict]
sources: [python-typing-guide]
last_updated: 2026-04-08
---

TypedDict is a class that provides type hints for dictionaries with specific keys. Used in WorldArchitect.AI for Firebase/Firestore data structures like CampaignData, StateUpdate, EntityData, and MissionData.

## Example
```python
class UserData(TypedDict):
    name: str
    email: str
    created_at: datetime
```

## Related
- [[PythonTypingGuide]] — usage guide
- [[Firebase]] — Firestore data operations
- [[TypeAliases]] — custom type aliases
