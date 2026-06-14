---
title: "2026-06-13 Levelup V2 Pr2 Routing Bridge"
type: source
tags: ["project", "worldarchitect", "level-up"]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_v2_pr2_routing_bridge.md
---

## Summary
Level-up v2 PR-2 (#7529) agents.py routing must use is_review_open OR is_session_active union bridge, not review_open alone — Codex P1 fix + the canonicalize_rewards fail-closed guarantee

## Key Claims
- PR-2 (#7529, branch feat/levelup-v2-routing, head 6882860759, bead rev-cuagv) swaps agents.py level-up routing onto the canonical `level_up_session`. Three sites (LevelUpAgent.matches_game_state, CharacterCreationAgent level-up arm, get_agent_for_input modal-lock) call a local `_level_up_session_active` helper.
- - v2-reducer sessions (`apply_level_up`, level_up_session.py:198) → `review_open=True`, NO `status` → caught by `is_review_open`.
- - model-path sessions (`apply_model_level_up_signal`, still live, called by rewards_engine.canonicalize_rewards) → active `status` (available/in_progress/committing/error), NO `review_open` → caught by `is_session_active` (level_up_session.py:88, status in ACTIVE_STATUSES).
- Fix = union: `is_review_open(gs) OR is_session_active(gs)`. Both read ONLY the canonical session (never legacy custom_campaign_state flags), so the "drop legacy custom_campaign_state.level_up_active" contract still holds. The `is_session_active` arm is the documented migration bridge — becomes dead/droppable once the model path moves to the reducer (PR-3/M-D), leaving `is_review_open` sole. See [[project_2026-06-13_levelup_v2_execution_spec_audit]].

## Connections
- [[project_2026-06-13_levelup_v2_execution_spec_audit]]
