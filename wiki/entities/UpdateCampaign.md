---
title: "UpdateCampaign"
type: entity
tags: [function, firestore, data-update]
sources: []
last_updated: 2026-04-08
---

## Description
Firestore service function that updates campaign documents. Supports both simple key updates and dot-notation path updates for nested field manipulation.

## Function Signature
```python
def update_campaign(user_id: str, campaign_id: str, updates: dict) -> bool
```

## Dot-Notation Feature
Allows updates like:
```python
{
    "game_state.custom_campaign_state.arc_milestones.wedding_tour": {
        "status": "completed",
        "phase": "ceremony_complete"
    }
}
```
Which creates nested structure:
```python
{
    "game_state": {
        "custom_campaign_state": {
            "arc_milestones": {
                "wedding_tour": {"status": "completed", "phase": "ceremony_complete"}
            }
        }
    }
}
```

## Related
- [[FirestoreService]] — parent module
- [[DotNotationPathUpdates]] — concept being implemented
