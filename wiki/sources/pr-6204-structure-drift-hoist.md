---
title: "PR #6204: fix(world-logic): hoist 5 fields out of rewards_box block"
type: source
tags: [worldarchitect-ai, world-logic, structure-drift, rewards-box, pr-6204]
date: 2026-04-11
source_file: mvp_site/world_logic.py
---

## Summary
5 fields were incorrectly nested inside `if hasattr(structured_response, "rewards_box"):` block in `world_logic.py:6707-6738`. They are now independent conditionals at the same level. This is the companion fix to PR #6197 (which only moved `debug_info`).

## Key Claims
Same root cause as PR #6197: checkpoint session fac29f6a4 (PR #2162) merged via PR #5782 placed fields inside the rewards_box block without noticing the existing fix at lines 6703-6705 for the same pattern on `action_resolution`.

## Fields Fixed

| Field | Before | After |
|-------|--------|-------|
| `social_hp_challenge` | Inside rewards_box block | Independent conditional |
| `recommend_spicy_mode` | Inside rewards_box block | Independent conditional |
| `recommend_exit_spicy_mode` | Inside rewards_box block | Independent conditional |
| `debug_info` | Inside rewards_box block + debug_mode | debug_mode only |
| `god_mode_response` | Inside rewards_box block | Independent conditional |

## Impact
- `debug_info` now emitted on all turns (fixes system warnings and dice roll display on narrative turns)
- `god_mode_response` available on all turns
- `social_hp_challenge` and spicy mode fields available without rewards_box

## Files Changed
- `.github/workflows/skeptic-cron.yml` (+173, -61)
- `.github/workflows/skeptic-gate.yml` (+74, -24)
- `docs/design/pr-designs/pr-6185.md` (+137, -0)
- `mvp_site/world_logic.py` (+32, -30)

## Connections
- [[StructureDriftPattern]] — direct case study; checkpoint from PR #2162 caused same nesting bug for multiple fields
- Related PRs: #6197 (debug_info fix, already merged), #6193 (normalizer), #5782 (checkpoint merge that introduced bug)
