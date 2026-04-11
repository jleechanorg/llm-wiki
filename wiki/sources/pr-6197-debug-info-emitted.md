---
title: "PR #6197: fix(debug_info): emit debug_info on all turns, not just when rewards_box present"
type: source
tags: [worldarchitect-ai, debug-info, world-logic, structure-drift, pr-6197]
date: 2026-04-11
source_file: mvp_site/world_logic.py
---

## Summary
`debug_info` was gated inside `if hasattr(structured_response, "rewards_box")`, so it was silently absent on turns with no combat/XP rewards (most turns), even when `debug_mode=True`. Moved to the outer `if structured_response:` block alongside `dice_rolls` and other per-turn fields.

## Key Claims
- `debug_info` only emitted when `rewards_box` was present — breaks debug mode on narrative-only turns
- Fix: move `debug_info` emission to outer `if structured_response:` block, gated only by `debug_mode=True`
- All other turns (without rewards_box) were silently dropping debug_info
- System warnings and dice roll display data unavailable on most gameplay turns

## Root Cause
Checkpoint session fac29f6a4 (PR #2162) merged via PR #5782 placed `debug_info` inside the rewards_box block without noticing an existing fix at lines 6703-6705 for the same pattern on `action_resolution`.

## Files Changed
- `mvp_site/tests/test_world_logic.py` (+147, -0)
- `mvp_site/world_logic.py` (+5, -3)

## Test Coverage
- `TestDebugInfoIndependentOfRewardsBox` added:
  - `test_debug_info_emitted_when_no_rewards_box` — confirms debug_info present even when LLM omits rewards_box
  - `test_debug_info_absent_when_debug_mode_off` — confirms no leakage when debug mode disabled

## Known Limitations
Does not address the separate dice_rolls/code_execution investigation (tracked separately, acknowledged in PR #6193).

## Connections
- [[StructureDriftPattern]] — direct case study: field nested inside wrong conditional block
- Related PRs: #6193 (normalizer), #6204 (hoist remaining 4 fields)
