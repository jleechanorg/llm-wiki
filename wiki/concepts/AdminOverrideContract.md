---
title: "Admin Override Contract"
type: concept
tags: [architecture, state-machine, zfc, worldarchitect]
---

A declarative contract that maps each admin/god-mode override action to the invariants it must establish post-execution. Prevents stale modal flags from persisting after admin short-circuits bypass state machine entry/exit protocols.

## Pattern

```python
ADMIN_OVERRIDE_CONTRACTS = {
    "god_mode_level_up": {
        "clear_flags": ["level_up_pending", "level_up_in_progress"],
        "assert_game_state": {"level": "target_level"},
    },
    "god_mode_character_creation": {
        "clear_flags": ["character_creation_in_progress"],
        "assert_game_state": {"character_creation_stage": None},
    },
}
```

## Why needed

Three separate PRs (#6844, #6842, #6825) independently discovered stale-flag bugs caused by admin short-circuits. Without a declarative contract, each override path must be individually audited.

## Related

- [[StaleFlag]] — the symptom
- [[ModalIntersection]] — intersection of concurrent modal systems
- [[ZeroFrameworkCognition]] — admin overrides violate server-ownership boundary
- [[WorldLogicStrip]] — where overrides live
