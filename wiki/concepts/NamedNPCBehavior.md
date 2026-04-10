---
title: "Named NPC Behavior"
type: concept
tags: [npc, game-state, behavior]
sources: [npc-death-state-persistence-tdd-tests]
last_updated: 2026-04-08
---

## Definition
NPCs identified as "named" based on having meaningful attributes (role other than generic enemy/minion, or backstory). Named NPCs should be preserved in npc_data with status: ["dead"] when killed, rather than deleted.

## Key Distinction
- **Named NPC**: Has role (merchant, assassin, etc.) or backstory attribute
- **Generic NPC**: Has only generic type "enemy" or "minion"
## Behavior
When a named NPC's hp_current reaches 0, cleanup_defeated_enemies marks them as dead (status: ["dead"]) instead of deleting their record from npc_data.
## Related
- [[NPC Death State Persistence]] — bug this behavior addresses
- [[GameState]] — manages NPC state
