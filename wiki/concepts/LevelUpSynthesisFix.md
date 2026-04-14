---
title: "LevelUpSynthesisFix"
type: concept
tags: [level-up, rewards-box, atomicity, D&D-5e, ASI, stuck-completion, world-logic]
sources: [pr-6275-synthesize-rewards-box]
last_updated: 2026-04-14
---

## Pattern

**Stuck-Completion Reconciliation**: When `custom_campaign_state.level_up_complete=True` but `rewards_box` is absent (or `planning_block` is absent), synthesize the missing field from canonical game state to satisfy the atomic pair contract.

```python
# Stuck state: level_up_complete=True but rewards_box missing
custom_state = game_state_dict.get("custom_campaign_state", {})
if _is_state_flag_true(custom_state.get("level_up_complete")):
    if not isinstance(rewards_box, dict):
        # Synthesize from XP/level data
        synthesized_box = build_level_up_rewards_box(game_state_dict, ...)
```

## Components

### 1. `ensure_level_up_rewards_box()`
Synthesizes a `rewards_box` when `level_up_complete=True` but box is absent. Extracts target level from `progression.resolved_target_level` or `player_character_data.level`, then calls `build_level_up_rewards_box()`. Also synthesizes a canonical planning_block with level-up choices.

**Status**: PR #6275 calls this function but `build_level_up_rewards_box` is undefined — **BLOCKER**.

### 2. `ensure_level_up_planning_block()`
Synthesizes a planning_block with `level_up_now` and `continue_adventuring` choices when `level_up_complete=True` but block is absent/invalid. Handles dict and JSON string planning_block inputs.

### 3. Stuck-Completion Detection in `_has_level_up_ui_signal()`
Extends signal detection to recognize `level_up_complete=True` + no `rewards_box` as an active level-up signal:

```python
return bool(
    _is_state_flag_true(custom_state.get("level_up_complete"))
    and not isinstance(rewards_box, dict)
)
```

### 4. D&D 5e ASI Injection in `_inject_levelup_choices_if_needed()`
At ASI levels (4, 8, 12, 14, 16, 19), injects 6 ability score improvement choices (`ASI_Strength`, `ASI_Dexterity`, `ASI_Constitution`, `ASI_Intelligence`, `ASI_Wisdom`, `ASI_Charisma`) alongside standard level-up choices.

**Known issue**: Tests fail because `is_level_up_active()` doesn't check `rewards_pending.level_up_available` — tests must set `custom_campaign_state.level_up_pending=True`.

### 5. Non-Level-Up Passthrough Fix
`_resolve_canonical_level_up_ui_pair` no longer calls `normalize_rewards_box_for_ui()` for non-level-up states, preventing default field pollution (`gold: 0`, `loot: []`, `source: ''`).

## Related
- [[LevelUpPolling]] — polling vs streaming architecture
- [[CanonicalCodePatterns]] — atomicity contract enforcement
- [[Level-Up D&D 5e Research]] — XP thresholds and ASI rules
- [[StreamingOrchestrator]] — streaming passthrough normalization
