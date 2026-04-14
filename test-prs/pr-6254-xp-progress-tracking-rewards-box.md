---
title: "PR #6254: [agento] fix(rewards): include XP progress tracking in rewards box visibility"
type: test-pr
date: 2026-04-14
pr_number: 6254
files_changed: [world_logic.py, test_rewards_box_normalizer_sentinel.py, test_modal_routing_fixtures.py, test_session_header_enrichment.py]
---

## Summary
Fixes `normalize_rewards_box_for_ui()` to include `current_xp` and `next_level_xp` in the `has_visible_content` check. Rewards boxes with `xp_gained=0` but valid XP progress tracking were being silently dropped, causing missing rewards UI and triggering atomicity cascade (suppressed box → scrubbed planning choices → missing level-up UI).

## Key Changes
- **world_logic.py**: Added `or (current_xp > 0 and next_level_xp > 0)` to `has_visible_content` check at line 171
- **test_rewards_box_normalizer_sentinel.py**: Added 4 test cases covering XP progress visibility edge cases
- Fixed campaigns: WQEl4sJb7RqWLndJK4GU, 3JM2gKc3eTFZHQnBtO8m, gufBO3EVc0GAp5LmVzWG, KtKlU0rOV6MmG3b6cOxd

## Diff Snippets
```python
# world_logic.py - has_visible_content now includes XP progress
has_visible_content = (
    (xp_gained and xp_gained > 0)
    or (current_xp > 0 and next_level_xp > 0)  # NEW CONDITION
    or (gold and gold > 0)
    or bool(loot)
    or level_up_available
    or (progress_percent and progress_percent > 0)
)
```

## Motivation
The frontend already handles XP progress with `hasProgress = current_xp != null && next_level_xp != null`, but the backend was killing the rewards box before it reached the frontend. This caused an atomicity enforcement cascade.