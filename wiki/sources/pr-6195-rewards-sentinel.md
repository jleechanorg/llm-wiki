---
title: "PR #6195: fix(rewards): restore has_visible_content gate with progress_percent support"
type: source
tags: [worldarchitect-ai, rewards, bug-fix, pr-6195]
date: 2026-04-11
source_file: .beads/issues.jsonl
---

## Summary
PR #6193 removed the `has_visible_content` gate from `normalize_rewards_box_for_ui` entirely, breaking the `None`-sentinel contract used by `_process_rewards_followup`. Restores the gate but adds `progress_percent > 0` as the actual missing condition from the original regression.

## Key Claims
- `NarrativeResponse._validate_rewards_box(None)` always returns `{}`, so `structured_response.rewards_box` is always a dict
- The check at world_logic.py:1767 relied on `normalize_rewards_box_for_ui({}) is None` as a sentinel
- PR #6193 broke this sentinel by removing the gate entirely
- Restoring gate in `mvp_site/rewards/builder.py` with `progress_percent > 0` added

## Root Cause
Without the gate, `normalize_rewards_box_for_ui({})` returns non-None, causing `rewards_already_in_response=True` for any primary response without rewards, silently skipping the rewards followup.

## Files Changed
- `mvp_site/rewards/builder.py` (+16, -1)
- `mvp_site/tests/test_rewards_box_normalizer_sentinel.py` (+115, -0)

## Evidence
- 157 reward tests pass
- Sentinel behavior: `normalize_rewards_box_for_ui({})` returns `None`
- `normalize_rewards_box_for_ui({"progress_percent": 50})` returns normalized dict

## Connections
- [[StructureDriftPattern]] — related structural bug where fields get nested inside wrong conditional blocks
- Related PRs: #6193 (normalizer fix, merged), #6192 (xp_gained=0 regression)
