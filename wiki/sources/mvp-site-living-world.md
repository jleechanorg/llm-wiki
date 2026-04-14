---
title: "mvp_site — Living World Trigger System"
type: source
tags: [worldarchitect-ai, living-world, turn-based, time-based, trigger-system]
date: 2026-04-14
source_file: raw/mvp_site_all/living_world.py
---

## Summary

Evaluates living world triggers based on either turn count intervals or elapsed game time. Prevents stale/corrupt tracking from disrupting the trigger cadence by realigning to the most recent interval boundary. Both a turn-based schedule (every N turns) and time-based schedule (every N hours) can fire independently or together.

## Key Claims

### Trigger Types
- **Turn-based**: fires every `turn_interval` turns (e.g., every 3 turns). Uses modulo to ensure consistent cadence: `(current_turn % turn_interval == 0) and (current_turn > normalized_last_turn)`
- **Time-based**: fires after `hours_elapsed >= time_interval` from last trigger
- **Combined**: both can fire simultaneously

### Corrupt Tracking Recovery
If `last_turn > current_turn` (stale data), realigns to most recent interval boundary:
```python
normalized_last_turn = current_turn - (current_turn % turn_interval)
```
This prevents corrupt tracking from permanently disabling living world events.

### Returns
`(should_trigger: bool, reason_string: str, hours_elapsed: float | None)`

Reason examples: `"turn (3 turns)"`, `"time (168.3h elapsed)"`, `"turn_and_time (6 turns, 72.1h)"`

## Connections

- [[LivingWorld]] — the living world feature this implements
- [[TurnInterval]] — the turn-based scheduling mechanism
- [[mvp-site-game-state]] — game state tracks turn count and time
- [[WorldTime]] — game time calculation that drives time-based triggers
