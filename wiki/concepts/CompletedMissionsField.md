---
title: "Completed Missions Field"
type: concept
tags: [data-field, missions, state-schema]
sources: []
last_updated: 2026-04-08
---

The completed_missions field is a campaign state field that tracks missions the player has finished. It stores completed mission objects with status "completed".

## Schema
```json
{
  "completed_missions": [
    {
      "mission_id": "sunderbrook_heist",
      "title": "Retrieve the Soul Vessel",
      "status": "completed"
    }
  ]
}
```

## Auto-initialization
The field is automatically initialized as an empty list when active_missions exists but completed_missions is missing. This ensures backward compatibility with older campaign states.

## Related
- [[MissionAutoCompletion]]
- [[ActiveMissionsField]]
- [[CampaignStateMigration]]
