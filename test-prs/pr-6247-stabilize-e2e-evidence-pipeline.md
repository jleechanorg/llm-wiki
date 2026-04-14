---
title: "PR #6247: fix(testing): stabilize e2e evidence pipeline and diagnostic scripts"
type: test-pr
date: 2026-04-13
pr_number: 6247
files_changed: [base_test.py, test_world_events_nesting_e2e.py, test_world_events_real_red_green.py, test_world_events_real_repro.py]
---

## Summary
Hardens end-to-end evidence generation pipelines that were experiencing CI hang regressions from unresolved subprocess unconsumed pipe buffering. Removes brittle `agg`/`ffmpeg` dependencies in artifact generation and enforces keyword-only arguments for campaign API endpoints in diagnostic scripts.

## Key Changes
- **base_test.py**: Replaced pipe management with `DEVNULL` routing via `_record_tmux_video` and removed `agg` processing inside `_stop_tmux_video`
- **test_world_events_real_repro.py**: Replaced positional arguments with keyword args for `get_campaign_world_events_state`
- **test_world_events_nesting_e2e.py**: Swapped process_turn and get_game_state wrappers for keyword-driven payload signatures
- **test_world_events_real_red_green.py**: Brought into compliance with keyword validation for user_id and campaign_id

## Motivation
CI hangs from video recording subprocess buffering, plus CodeRabbit-reported crashes from positional argument usage in diagnostic scripts.