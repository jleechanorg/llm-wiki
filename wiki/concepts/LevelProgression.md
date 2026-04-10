---
title: "Level Progression"
type: concept
tags: [character-progression, game-mechanics, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Level Progression in WorldArchitect.AI requires displaying character levels in narrative when mentioning character names (e.g., "Theron (Lvl 5)", "the level 3 rogue"). XP awards must be stated in narrative text, not just state updates.

**Requirements**:
- Display level with character name in narrative
- Show level progression incrementally
- Announce level-ups in narrative text
- Never skip levels in progression (Level 1 → Level 2 → Level 3)

**Related Concepts**:
- [[DeferredRewardsProtocol]] — catch missed XP/loot
- [[VisibilityRule]] — XP in narrative, not just state
- [[EntityIDSchema]] — character entity format
