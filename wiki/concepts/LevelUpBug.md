---
title: "Level-Up Bug Chain"
type: concept
tags: [worldarchitect-ai, bug-chain, level-up, rewards-box, structure-drift, atomicity]
sources: [pr-6161-fix-rewards-box-planning-block-atomicity-and-get-c, pr-6161-bug-hunt-report, pr-6179-fix-living-world-inject-persisted-world-events-for, pr-6193-fix-rewards-stop-dropping-rewards-box-payloads-wit, pr-6194-investigate-dice-rolls-debug-messages-regression-p, pr-6195-fix-rewards-restore-has-visible-content-gate-with, pr-6196-dragon-knight-rewards-box, pr-6204-fix-world-logic-hoist-5-fields-out-of-rewards-box, pr-6165-launch-cta-level-up]
last_updated: 2026-04-11
---

## Summary

The level-up bug chain is a sequence of 8+ PRs addressing cascading bugs in worldarchitect.ai's rewards_box and level-up system. The root issue spans three weeks of regressions involving structure drift, atomicity violations, and debug-gating that prevented non-debug users from seeing dice rolls and debug messages.

## Bug Chain Overview

| PR | Title | Issue |
|----|-------|-------|
| #6161 | rewards_box/planning_block atomicity | Original atomicity fix — missing rewards_box in extraction, TypeErrors in polling paths |
| #6179 | living world debug gate removed | `inject_persisted_living_world_fallback` was debug_mode-gated, blocking non-debug users |
| #6193 | stop dropping rewards_box payloads | PR #6161 normalizer over-aggressively filtered payloads with only level_up/progress |
| #6194 | investigate dice/debug regression | Dice rolls and debug_info don't render for non-debug users (investigation open) |
| #6195 | restore has_visible_content gate | PR #6193 removed gate entirely, breaking _process_rewards_followup sentinel contract |
| #6196 | dragon knight rewards_box | PR #6137 template bypass silently dropped FIELD_REWARDS_BOX |
| #6204 | hoist 5 fields from rewards_box block | Structure drift: 5 fields nested inside rewards_box block (checkpoint PR #2162) |
| #6165 | launch CTA + level-up atomicity | Wizard CTA hidden + stale level-up choices during polling |

## Root Causes

### 1. Structure Drift (PR #2162 → PR #5782)
Checkpoint session placed `debug_info` inside `if hasattr(structured_response, "rewards_box"):` block. Affects: `debug_info`, `social_hp_challenge`, `spicy_mode` fields, `god_mode_response`.

**Fix:** PR #6197, #6201, #6204 progressively un-nest fields.

### 2. Atomicity Violations
`rewards_box` and `planning_block` must be consistent with each other and with game state. Six distinct bugs found:
- Stale planning_block not written back after enforcement
- Polling path discarding valid non-level-up choices
- False-positive level-up choice scrubbing in think mode
- Spurious modal finish injection when planning_block was None

**Fix:** PRs #6161, #6192, #6195, #6201.

### 3. Debug Gating
Frontend debug-gated dice rolls and debug messages, but backend also had debug_mode gates. Non-debug users saw nothing.

**Fix:** PRs #6179 (living world), PR #6204 (debug_info hoist).

## Key Files

- `mvp_site/world_logic.py` — Contains all atomicity logic, polling paths, rewards_box assembly
- `mvp_site/rewards/` — New module (PR #6161) with `domain.py`, `builder.py`, `resolver.py`, `triggers.py`
- `mvp_site/rewards/builder.py:normalize_rewards_box_for_ui()` — Normalizer with has_visible_content sentinel
- `mvp_site/world_logic.py:_process_rewards_followup()` — Uses sentinel contract with normalizer

## Key Sentinels

The `_process_rewards_followup` function relies on `normalize_rewards_box_for_ui({}) is None` as a sentinel for "no rewards present". PR #6193 broke this by removing the gate entirely. PR #6195 restored it with `progress_percent > 0` added.

```python
# The sentinel contract:
normalize_rewards_box_for_ui({})  # returns None when no visible content
normalize_rewards_box_for_ui({"progress_percent": 50})  # returns normalized dict
```

## Connections

- [[StructureDriftPattern]] — Root cause of field nesting
- [[LevelUp]] — Level-up modal and flag management
- [[RewardsBox]] — rewards_box JSON structure
- [[RewardsBoxAtomicity]] — Atomicity helper function
- [[dice_rolls]] — Dice roll display (still investigating regression)
