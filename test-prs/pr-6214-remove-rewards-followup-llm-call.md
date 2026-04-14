---
title: "PR #6214: fix: remove rewards followup LLM call"
type: test-pr
date: 2026-04-13
pr_number: 6214
files_changed: [world_logic.py, test_world_logic.py, test_rewards_box_normalizer_sentinel.py, pr-6214.md, rewards-single-call-architecture.md]
---

## Summary
Optimization PR that removes the defensive 2nd LLM call (`_process_rewards_followup`) fired when reward events are pending but the primary LLM response lacks a rewards_box. Replaces it with a deterministic server-side postcondition (`_enforce_primary_rewards_box_postcondition`) that synthesizes the canonical rewards_box from game state or fails closed.

## Key Changes
- Removed `_process_rewards_followup()` (~190 lines) - the async 2nd Gemini call
- Added `_enforce_primary_rewards_box_postcondition()` - deterministic check
- Added `_response_has_displayable_rewards_box()`, `_xp_increased()`, `_requires_primary_rewards_box()`
- Added canonical level-up synthesis: `_project_level_up_ui_from_game_state()` builds rewards_box from rewards_pending
- Fixed postcondition ordering: check runs AFTER `_detect_rewards_discrepancy` (sets rewards_processed=True)

## Diff Snippets
```python
# Removed: ~190 lines of async followup call
# Added: synchronous postcondition enforcement
def _enforce_primary_rewards_box_postcondition(unified_response, game_state_dict):
    if _requires_primary_rewards_box(unified_response, game_state_dict):
        if not _response_has_displayable_rewards_box(unified_response):
            # Synthesize from canonical state or raise
            ...
```

## Motivation
The 2nd LLM call added ~3-10s latency and doubled API cost for rewards-eligible turns. Replaced with deterministic server-side enforcement that fails closed (raises RuntimeError if rewards would be invisible) rather than silently losing rewards.