---
title: "State Flag Semantics"
type: concept
tags: [state, flags, semantics, worldai]
last_updated: 2026-04-14
---

## Summary

State flags are boolean signals stored alongside entity state that trigger side effects when set. Understanding their exact semantics — when they can be set, cleared, and how they interact — is critical to preventing state machine bugs.

## Flag Lifecycle

```
[UNSET] --set()--> [SET]
[SET] --clear()--> [UNSET]
[SET] --expire()--> [STALE]
[STALE] --acknowledge()--> [SET]  (re-triggers action)
```

## Key Semantics Rules

### 1. Idempotent Sets
Setting a flag that's already SET is a no-op:
```python
def set_flag(flag: StateFlag) -> None:
    if flag.state == FlagState.SET:
        return  # Already set, no change
    flag.state = FlagState.SET
    flag.timestamp = now()
```

### 2. Clear Before Re-set
Before re-setting a flag, always clear it first:
```python
def acknowledge_and_clear(flag: StateFlag) -> None:
    flag.state = FlagState.UNSET
    flag.timestamp = None
```

### 3. Stale Detection
Flags older than `STALE_THRESHOLD` are considered stale:
```python
STALE_THRESHOLD = timedelta(hours=24)

def is_stale(flag: StateFlag) -> bool:
    if flag.state != FlagState.SET:
        return False
    return now() - flag.timestamp > STALE_THRESHOLD
```

## Level-Up Specific Flags

| Flag | Meaning | Stale behavior |
|------|---------|----------------|
| `has_level_up_signal` | LLM indicated level-up | Suppress new level-ups if stale |
| `level_up_acknowledged` | User saw modal | Clear after confirmation |
| `rewards_processed` | Rewards computed | Never stale |

## Connections
- [[StateTransitions]] — State transition patterns
- [[LevelUpArchitecture]] — Level-up state machine
- [[StateModification]] — State mutation patterns
