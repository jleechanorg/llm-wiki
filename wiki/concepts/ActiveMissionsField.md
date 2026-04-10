---
title: "Active Missions Field"
type: concept
tags: [data-field, missions, state-schema]
sources: []
last_updated: 2026-04-08
---

The active_missions field is a campaign state field that tracks missions currently in progress. When the LLM narrative indicates a mission is complete, it is moved from active_missions to [[CompletedMissionsField]].

## Schema
```json
{
  "active_missions": [
    {
      "mission_id": "sunderbrook_heist",
      "title": "Retrieve the Soul Vessel",
      "status": "active",
      "objective": "Raid vault and transfer souls"
    }
  ]
}
```

## Lifecycle
1. Mission created → added to active_missions
2. Mission in progress → remains in active_missions
3. Mission completed → moved to completed_missions, removed from active_missions

## Related
- [[MissionAutoCompletion]]
- [[CompletedMissionsField]]
