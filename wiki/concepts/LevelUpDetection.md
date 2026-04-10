---
title: "Level-Up Detection"
type: concept
tags: [game-mechanics, progression, level-up]
sources: [deferred-rewards-protocol]
last_updated: 2026-04-08
---

Level-Up Detection is the automatic system that triggers when deferred XP pushes a player to their level-up threshold.

## Trigger Conditions

When deferred rewards push `current_xp` >= `next_level_xp`:

1. Set `level_up_available: true` in rewards_box
2. Include level-up offer in narrative
3. Provide planning_block choices for level-up

## Example rewards_box with Level-Up

```json
{
  "xp_gained": 200,
  "current_xp": 900,
  "next_level_xp": 900,
  "level_up_available": true
}
```

## Related Concepts

- [[Deferred Rewards Protocol]] — protocol that detects level-ups
- [[Rewards Box]] — includes level_up_available flag
- [[Character Creation Level-Up Mode]] — handles the level-up flow
