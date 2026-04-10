---
title: "Campaign State Migration"
type: concept
tags: [migration, backward-compatibility, state-management]
sources: []
last_updated: 2026-04-08
---

Campaign State Migration is the process of transparently updating legacy campaign states to support new features without requiring manual intervention.

## Example: completed_missions
- Older campaigns have active_missions but lack completed_missions
- When state changes are applied, completed_missions is auto-initialized
- No manual god mode intervention required
- Migration happens transparently during normal gameplay

## Benefits
- No data loss for existing campaigns
- Seamless feature adoption
- No forced migration or data conversion prompts

## Related
- [[MissionAutoCompletion]]
- [[Nocturne]] — production campaign that required this fix
