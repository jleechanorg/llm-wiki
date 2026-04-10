---
title: "Nocturne"
type: entity
tags: [campaign, game, production]
sources: []
last_updated: 2026-04-08
---

Nocturne is a production campaign in WorldArchitect that experienced a bug where missions would not auto-complete. The campaign had active_missions but was missing the completed_missions field, causing missions to stay in active_missions even after narrative completion.

## Bug Context
- Campaign had active_missions but no completed_missions field
- Missions remained in active_missions after narrative completion
- Required manual god mode intervention to close missions
- Fixed by auto-initializing completed_missions when active_missions exists

## Related
- [[MissionAutoCompletion]]
- [[CompletedMissionsField]]
- [[CampaignStateMigration]]
