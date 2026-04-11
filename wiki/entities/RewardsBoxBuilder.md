---
title: "RewardsBoxBuilder"
type: entity
tags: [worldarchitect-ai, file, python, rewards, module]
sources: [pr-6161-fix-rewards-box-planning-block-atomicity-and-get-c, pr-6193-fix-rewards-stop-dropping-rewards-box-payloads-wit, pr-6195-fix-rewards-restore-has-visible-content-gate-with]
last_updated: 2026-04-11
---

## Summary

`mvp_site/rewards/builder.py` is part of the new `mvp_site/rewards/` module introduced by PR #6161. It contains `normalize_rewards_box_for_ui()` which normalizes rewards_box payloads for frontend display and implements the `has_visible_content` sentinel.

## Key Function

### `normalize_rewards_box_for_ui(input_dict)`

Normalizes rewards_box payloads for UI display. Returns `None` for empty/invisible payloads, normalized dict otherwise.

**The Sentinel Contract:**
```python
normalize_rewards_box_for_ui({})  # returns None — empty dict has no visible content
normalize_rewards_box_for_ui({"progress_percent": 50})  # returns normalized dict — progress_percent > 0 is visible
normalize_rewards_box_for_ui({"xp_gained": 0})  # returns None — zero values not visible
normalize_rewards_box_for_ui({"gold": 100})  # returns normalized dict — gold > 0 is visible
```

**Why the Sentinel Matters:**
`_process_rewards_followup` in `world_logic.py` uses `normalize_rewards_box_for_ui({}) is None` as a sentinel to detect "no rewards present". When this returns non-None for empty dicts, it causes `rewards_already_in_response=True` for any primary response without rewards, silently skipping the rewards followup.

**The Bug (PR #6193):**
PR #6193 removed the `has_visible_content` gate entirely, breaking the sentinel contract. PR #6195 restored the gate but added `progress_percent > 0` as the actual missing condition.

## Related Files in `mvp_site/rewards/` Module

- `__init__.py` — Module exports
- `domain.py` — Data classes for rewards
- `builder.py` — UI payload builders (this file)
- `resolver.py` — Level progression logic
- `triggers.py` — Pending rewards triggers

## Connections

- [[LevelUpBug]] — Full bug chain context
- [[RewardsBoxAtomicity]] — Atomicity helpers
- [[RewardsBox]] — rewards_box JSON structure
