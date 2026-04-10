---
title: "Continuity Locks"
type: concept
tags: [continuity, scene-tracking, narrative, state-management]
sources: ["preventing-scene-backtracking-god-mode-corrections"]
last_updated: 2026-04-07
---

## Description
Mechanism to prevent scene rewinds by tracking continuity fingerprints after each accepted turn. Includes `last_scene_id`, `last_location`, and active entities in next prompt as "do not rewind" anchors.

## Implementation
- Track `last_scene_id`, `last_location`, active entities in `custom_campaign_state`
- Include fingerprint in next prompt
- [[NarrativeSyncValidator]] auto-adjusts minor regressions by merging prior state
- Severe conflicts trigger internal reshot with forward-only reminder

## References
- [[GameState]] — stores continuity fingerprints
- [[NarrativeSyncValidator]] — enforces forward-only narrative flow
