---
name: project_2026-06-13_levelup_v2_pr6_gate_closeout
description: "Level-up v2 PR-6 (#7533 god-mode fold) gate closeout — HEAD 169d0d578b, tests GREEN, evidence refreshed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 40c57912-2a0f-484a-8bf6-7a2664223678
---

Level-up v2 PR-6 (#7533) — god-mode admin commit folded onto v2 `apply_level_up()`.

HEAD `169d0d578b958ac8e86d5debf0b1a93fab477e87` (local == origin == PR head; no new
commit to push — impl already landed). Branch `feat/levelup-v2-godmode-fold`,
worktree `~/.lvl-lanes/wt-lvl-pr6`.

**What it does:** `_god_mode_level_up_dispatch` (god_mode_level_up.py:186 Path A, :247
mixed-contract admin-win) routes through `apply_level_up(source="god_mode_admin")`
instead of writing `level_up_session` directly. Partial PCD delta → `level_facts["sheet"]`
→ R4 recursive deep-merge. Stale `rewards_box.level_up_available` stripped from BOTH
`structured_fields` AND `new_game_state` (god_mode_level_up.py:212-213, :292-293).
Non-finish invariant gated behind `_dispatched_admin_commit` (world_logic.py:8964);
canonicalize_rewards likewise gated (world_logic.py:8836).

**Gate results (verified by me):**
- Tests: 64 deterministic / 222 level-up unit / 579 game_state+rewards / 3 god-mode E2E — 0 regressions.
- 1 pre-existing out-of-lane fail = `test_full_lifecycle_walk_all_five_stages` (test_end2end/test_level_up_reducer_fixture_replay.py); CONFIRMED fails identically at merge-base b26a5eb1 (`assert 2 == 1`, line 406).
- Broad single-process 29-file run surfaces a 2nd red, `test_get_agent_for_input_ignores_stale_rewards_routing`, that PASSES alone + in-file — known CI-immune cross-file isolation leak (same pattern as [[project_2026-06-13_pr7531_pr4_gate_state]]), NOT a PR-6 regression.
- /code_standards: `apply_level_up` (level_up_session.py:123-208) is pure copy-on-write atomic co-write (PCD+session on one new_state); both god-mode sites single-writer through it. Pre-existing multi-writer debt (source="server" organic writer, unwired projector PR-7, orphaned v1 apply_god_mode_admin_commit) flagged as follow-ups.
- Ruff clean on all 3 changed source files.
- Holdout: sealed/operator-run — NOT executed by agent.
- /er evidence gist REFRESHED to current HEAD with honest (a)-(d) coverage: gist 8bc9a5429b3f8979adf3031293a4c9e1 (linked in PR body; 2nd gate_er gist 5468b80326b also linked). Gate 0 satisfied (.md link inside `## Tenets`).
- spec.md + .dark-factory/ correctly NOT pushed (lane-local).

Spec AC table names some tests aspirationally (test_dispatched_admin_commit_suppresses_canonicalize, test_non_finish_invariant_gated_by_dispatched_admin_commit, test_stale_rewards_box_stripped_from_new_game_state) that DON'T literally exist — the behaviors are really covered by `test_end2end/test_god_mode_level_up_split_end2end.py` (3 tests) + `test_god_mode_levelup_v2_fold.py` (4 tests). Cite real names, not AC names.

Related: [[project_2026-06-13_levelup_v2_pr5_gate_closeout]], [[project_2026-06-13_levelup_v2_dark_factory_gate_pipeline]].
