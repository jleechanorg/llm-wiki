---
name: project_2026-06-13_levelup_v2_pr2_routing_bridge
description: "Level-up v2 PR-2 (#7529) agents.py routing must use is_review_open OR is_session_active union bridge, not review_open alone — Codex P1 fix + the canonicalize_rewards fail-closed guarantee"
metadata: 
  node_type: memory
  type: project
  originSessionId: 330aa8ac-564f-4217-aa44-6f7452e0fbc5
---

PR-2 (#7529, branch feat/levelup-v2-routing, head 6882860759, bead rev-cuagv) swaps agents.py level-up routing onto the canonical `level_up_session`. Three sites (LevelUpAgent.matches_game_state, CharacterCreationAgent level-up arm, get_agent_for_input modal-lock) call a local `_level_up_session_active` helper.

**Codex P1 (real): routing on `is_review_open` ALONE drops status-only sessions.** During the PR-2/3/4 migration two session shapes coexist:
- v2-reducer sessions (`apply_level_up`, level_up_session.py:198) → `review_open=True`, NO `status` → caught by `is_review_open`.
- model-path sessions (`apply_model_level_up_signal`, still live, called by rewards_engine.canonicalize_rewards) → active `status` (available/in_progress/committing/error), NO `review_open` → caught by `is_session_active` (level_up_session.py:88, status in ACTIVE_STATUSES).
Fix = union: `is_review_open(gs) OR is_session_active(gs)`. Both read ONLY the canonical session (never legacy custom_campaign_state flags), so the "drop legacy custom_campaign_state.level_up_active" contract still holds. The `is_session_active` arm is the documented migration bridge — becomes dead/droppable once the model path moves to the reducer (PR-3/M-D), leaving `is_review_open` sole. See [[project_2026-06-13_levelup_v2_execution_spec_audit]].

**Key durable guarantee: `rewards_engine.canonicalize_rewards` FAILS CLOSED (rewards_engine.py:3497-3506).** If no backing `level_up_session` lands (stale guard, reducer rejection, GameState-non-dict, empty delta) it calls `_clear_orphan_level_up_meta` AND strips `rewards_box.level_up_available=False` + pops `new_level`. ⇒ In production v2 a level-up pending/offer state can NEVER exist without a canonical session. So "legacy flags / rewards_pending without a session" is an IMPOSSIBLE production shape — pre-session-machine test fixtures asserting it route are obsolete.

**Test fallout of the swap:** the routing swap broke 19 pre-existing tests (11 in test_agents.py + 8 across test_agent_routing_with_state_validation, test_modal_integration, test_modal_routing_fixtures.py/.json, test_level_up_stale_guards) that asserted legacy-flag routing without a session. Fixed by adding canonical `level_up_session` (model-path shape: status/current_level/target_level/source) to fixtures; the 2 testing removed legacy mechanics (string-typed flags, nested-flag fallback) rewritten to v2 contract. Shared harnesses (test_modal_base.assert_routing_matches_injection, test_modal_routing_fixtures._mock_game_state) needed `level_up_session` propagation onto the Mock/SimpleNamespace or routing never sees it.

**Pre-existing / out-of-lane failures on this branch (NOT caused by PR-2, verified at pre-swap agents.py c5f66c45ea):** test_agents.py::TestSchemaInjection::* (prompt-content; branch changed no prompts vs merge-base b26a5eb1e9) and test_agent_routing_with_state_validation::test_cc_finish_choice_routes_directly_to_story_before_cc_agent (CC conclude routing). test_levelup_v2_schema FileNotFoundError is a cwd artifact — run from repo root, not mvp_site/.
