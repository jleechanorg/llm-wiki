---
title: "PR 4 god-mode split: CodeRabbit review loop pattern"
type: source
tags: [level-up, god-mode, code-review, pr-7376, reducer-frozen, worldarchitect-ai]
date: 2026-06-09
source_file: raw/project_2026-06-09_pr4_god_mode_split_cr_loop.md
---

## Summary
PR #7376 (god-mode contract split) CodeRabbit caught two call-site defects (heads 1d39614088 + 510e17148f). When a dispatcher returns a NEW updated_game_state_dict, the caller's local rebind is not enough — captured references (lambdas, callbacks) still point to OLD dict. Fix pattern: clear-and-update in place preserves dict identity. Two parallel fail-closed paths must stay symmetric — branch drift between sibling rejection paths is a silent-failure class. Reducer in level_up_session.py is FROZEN post PR 1-3 merge; PR 4 can only CALL into it (don't get drawn into while-I'm-here edits). Phantom rewards_box.level_up_available after admin commit requires symmetric _strip_level_up_rewards_box_offer helper in both Path A success and mixed-contract success branches.

## Key Claims
- When dispatcher returns NEW updated_game_state_dict, caller's local rebind is not enough — captured references (lambda, callback) still point to OLD dict; fix = clear-and-update in place
- Two parallel fail-closed paths in _god_mode_level_up_dispatch drifted: branch 2 stripped level_up_signal/modal choices from structured_fields, branch 3 did not
- CR workflow re-review cadence: push fix → gh workflow run green-gate.yml -f pr_number=N -f head_sha=SHA (BOTH required — head_sha alone gives 422) → @coderabbitai please re-review → wait for reviewDecision to flip
- Reducer in level_up_session.py is FROZEN post PR 1-3; PR 4 can only CALL into it
- Phantom rewards_box.level_up_available after admin commit: model emits it in same turn as admin commit closes session; if not stripped, frontend renders phantom level-up prompt

## Connections
- [[project_2026-06-08_level_up_session_state_machine_pivot]]
- [[GodModeDispatcher]]
- [[CodeRabbitReReviewCadence]]
- [[PhantomRewardsBox]]
