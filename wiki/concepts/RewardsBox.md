---
title: "Rewards Box"
type: concept
tags: [json-structure, game-output, rewards]
sources: [deferred-rewards-protocol]
last_updated: 2026-04-08
---

The `rewards_box` is a JSON structure included in LLM responses when awarding deferred XP/loot.

## Structure

```json
{
  "source": "deferred",
  "deferred_reason": "Missed combat rewards from Scene 5",
  "xp_gained": 50,
  "current_xp": 350,
  "next_level_xp": 900,
  "progress_percent": 38,
  "level_up_available": false,
  "loot": ["Items missed earlier"],
  "gold": 0
}
```

## Fields

| Field | Purpose |
|-------|--------|
| `source` | Always "deferred" to indicate catch-up rewards |
| `deferred_reason` | Explains what was missed |
| `xp_gained` | Amount of XP being awarded |
| `current_xp` | Player's total XP after award |
| `next_level_xp` | XP needed for next level |
| `progress_percent` | Progress toward next level |
| `level_up_available` | True if threshold reached |
| `loot` | Array of items awarded |
| `gold` | Gold amount awarded |

## Related Concepts

- [[Deferred Rewards Protocol]] — protocol that generates rewards_box
- [[Rewards Processed Flag]] — prevents duplicate awards
