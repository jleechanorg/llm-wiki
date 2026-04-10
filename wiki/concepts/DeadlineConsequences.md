---
title: "Deadline Consequences"
type: concept
tags: [game-mechanic, penalty, narrative-consequence]
sources: ["time-pressure-game-state"]
last_updated: 2026-04-08
---

## Definition
Deadline consequences are narrative and mechanical outcomes that trigger when a time-sensitive event's deadline passes without the player completing the required objective.

## Examples
- **rescue_merchant**: "Merchant will be sold to slavers"
- **save_village**: "Half the village dies from plague"

## Implementation
Consequences are checked by comparing current game time (world_time.day) against deadline time (deadline.day). If current_day > deadline_day, the consequence triggers.

## Related Concepts
- [[TimeSensitiveEvents]] — the mechanism that triggers consequences
- [[UrgencyLevels]] — determines severity and warning timing
