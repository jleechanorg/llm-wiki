---
title: "SystemMessageEmissionPath"
type: concept
tags: [system-messages, rewards-box, pipeline, worldarchitect]
sources: [jleechan-orke]
last_updated: 2026-04-12
---

## Summary

`SystemMessageEmissionPath` is the recognition that system messages are a separate pipeline from `rewards_box`, not part of the rewards pipeline. Conflating them causes structure drift and modal routing bugs.

## The Distinction

| Aspect | System Messages | Rewards Box |
|--------|---------------|-------------|
| Pipeline | Separate `debug_info.system_message` path | `rewards/` module pipeline |
| Trigger | `debug_mode=True` + LLM emits system | `rewards_pending` present |
| Rendering | `app.js` debug mode section | `rewards_box` modal |

## Why It Matters

The LevelUpBug investigation found that `debug_info` was incorrectly nested inside the `rewards_box` gate. System messages (the `system_message` field in `debug_info`) should emit independently of whether `rewards_box` is present.

## Correct Pattern

System messages flow through `debug_info.system_message` regardless of rewards_box state:
```python
if debug_mode and hasattr(structured_response, 'debug_info'):
    unified_response['debug_info'] = structured_response.debug_info
# No dependency on rewards_box
```

## Related

- [[RewardsBoxAtomicity]] — Atomicity invariants for rewards_box
- [[LevelUpBug]] — Full bug chain context
- [[SystemInstruction]] — System instruction handling
