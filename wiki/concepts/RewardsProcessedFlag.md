---
title: "Rewards Processed Flag"
type: concept
tags: [state-tracking, deduplication, game-state]
sources: [deferred-rewards-protocol]
last_updated: 2026-04-08
---

The `rewards_processed` flag is a boolean state indicator that prevents double-counting of XP and loot rewards.

## Usage

Embedded in game state structures:
- `combat_state.rewards_processed`
- `encounter_state.rewards_processed`

## Protocol

1. Before awarding ANY reward, check if `rewards_processed: true`
2. If true, SKIP the reward (already processed)
3. If false, award the reward and set `rewards_processed: true`
4. Include state updates in response to persist the flag

## Example State Update

```json
{
  "state_updates": {
    "combat_state": {
      "rewards_processed": true
    },
    "encounter_state": {
      "rewards_processed": true
    }
  }
}
```

## Related Concepts

- [[Deferred Rewards Protocol]] — protocol that uses this flag
- [[XP Verification]] — secondary heuristic when flag is missing/ambiguous
