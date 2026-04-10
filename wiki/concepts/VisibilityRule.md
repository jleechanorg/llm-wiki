---
title: "Visibility Rule"
type: concept
tags: [protocol, player-experience, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Visibility Rule defines what players can and cannot see in WorldArchitect.AI. Players see ONLY narrative text — state_updates and rewards_pending are invisible to them.

**What Players See**:
- Narrative text (response content)
- Explicit announcements (e.g., "You gain X XP!")

**What Players Don't See**:
- state_updates
- rewards_pending
- Internal tracking data

**Consequence**: XP awards and level-ups MUST be stated explicitly in narrative text, not just recorded in state

**Related Concepts**:
- [[LevelProgression]] — XP in narrative requirement
- [[GameStateManagement]] — state update format
- [[SessionHeader]] — visible status information
