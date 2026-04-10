---
title: "Dice System Requirement"
type: concept
tags: [dice, dnd-5e, game-mechanics]
sources: []
last_updated: 2026-04-08
---

## Definition
Mandatory dice rolling rule: ALL attacks and saving throws REQUIRE dice rolls. Dice results MUST appear ONLY in action_resolution.mechanics.rolls JSON, NEVER in narrative text.

## Key Rules
- MANDATORY: Roll dice for ALL attacks and saves
- NEVER skip or fabricate dice rolls
- NEVER show dice in narrative: no `[Attack: 15 vs AC 16]`, no `(rolled 8)`
- ONLY roll damage if attack hits (no damage rolls on miss)

## Implementation
Dice rolls stored in:
```json
{
  "action_resolution": {
    "mechanics": {
      "rolls": [...]
    }
  }
}
```

## Related Concepts
- [[CombatSystemProtocol]] — parent protocol
- [[InitiativeOrder]] — where dice are rolled during turns
