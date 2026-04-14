---
title: "Rewards Engine Idempotency"
type: concept
tags: [level-up, rewards, architecture, idempotency]
sources: [level-up-engine-v4-design]
last_updated: 2026-04-14
---

## Definition

`rewards_engine.canonicalize_rewards()` **must be idempotent**: calling it twice with the same inputs MUST produce the same outputs. Formally: `canonicalize(x, y, z) == canonicalize(x, y, z)` regardless of how many times called.

## Why Idempotency Matters

This requirement is critical because [[DeferredRewardsProtocol]] calls `rewards_engine` every 10 player turns (`turn_number % 10 == 0`) to fill in missed rewards. If the engine were not idempotent, successive calls would compound rewards or corrupt state.

### The Idempotency Invariant

```
for all (structured_fields, game_state_dict, original_state_dict):
    result1 = canonicalize_rewards(...)
    result2 = canonicalize_rewards(...)
    assert result1 == result2
```

### What This Means Practically

- **No side effects**: `canonicalize_rewards()` must be a pure function (or at minimum, produce the same observable output for the same inputs)
- **No mutation of inputs**: The function must not modify `structured_fields`, `game_state_dict`, or `original_state_dict`
- **No stateful accumulation**: Calling twice must NOT double-count XP or add duplicate loot
- **Stable output**: `normalize_rewards_box()` called twice on the same input produces the same normalized output

## Implementation Requirements

The v4 design achieves idempotency through:

1. **Single call per request** — the pipeline calls `rewards_engine` exactly once, not twice
2. **Pre-LLM snapshot comparison** — `original_state_dict` snapshot captures state BEFORE the LLM call so that repeated calls can detect staleness
3. **Clean type normalization** — `normalize_rewards_box()` is a pure transformation with no branching on prior state
4. **Atomic pair enforcement** — `rewards_box` + `planning_block` are always returned as a pair or (None, None), never partially

## Known Violations Fixed in v4

| Bug | Cause | Fix |
|-----|-------|-----|
| Double normalization in non-streaming path | `normalize_rewards_box_for_ui()` called twice (lines 6808-6882 and 7250-7317) | Single `canonicalize_rewards()` call, result used for both persistence and response |
| Streaming passthrough bypass | `streaming_orchestrator.py:709` unconditional passthrough skips `normalize_rewards_box_for_ui` | Single pipeline via `llm_parser.py`; no passthrough path |

## Related Concepts

- [[DeferredRewardsProtocol]] — calls rewards_engine every 10 turns, requires idempotency
- [[SingleResponsibilityPipeline]] — the pipeline that calls rewards_engine exactly once
- [[RewardsBoxAtomicity]] — atomic pair enforcement within the idempotent scope
- [[DefensiveNumericConversion]] — pure type normalization (inherently idempotent)
