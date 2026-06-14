---
name: project-2026-06-13-pr7531-pr4-gate-state
description: "Level-up v2 PR-4 (#7531 world_logic) gate-run state + cross-file test-isolation leak finding"
metadata: 
  node_type: memory
  type: project
  originSessionId: b02a0ef1-c69d-4d00-87b0-083d5297f59f
---

PR #7531 = level-up v2 PR-4 (route world_logic.py grant→`apply_level_up`, finish→`close_review`; delete source=server 2nd-writer). Stacks on PR-1 (#7521). Head `b247850137` on feat/levelup-v2-world-logic (local==origin==PR head). Refreshed gate evidence gist `675a0bac`.

**Gate closeout 2026-06-13 (this session):** No code regression — addressed an EVIDENCE gap only. Body had claimed "1 pre-existing failure"; verified at merge-base `b26a5eb1` there are actually **3** (full_lifecycle_walk_all_five_stages + 2× test_modal_integration_end2end: first_turn_level_up_pending_routes_and_freezes_time, level_up_now_expands_from_unsanitized_routing_state). All 3 fail at merge-base with this lane's commits absent; the end2end files are unmodified by the lane (separate end2end CI job). Fixed via body edit disclosing all 3 + linking refreshed gist. Lane files + co-resident files run together in one process = 572 passed, 0 failed (the broad-`-k` leak does NOT occur per-file). test_levelup_v2_schema.py FileNotFoundError is a CWD artifact (path is repo-root relative; 3 passed from repo root).

**Gate verdict (2026-06-13):**
- Code-standards (single-writer + normalization atomicity): PASS. Only two `state_changes["level_up_session"]=` writes (world_logic.py:2817 grant, :3006 finish), both reducer outputs. `_build_level_up_facts` (2409) is read-only. No `source=server`, no old `_build_level_up_session_update`. The :2367 write is defensive original-session preservation, not a writer.
- Tests under CI's real model (per-file: `run_tests.sh` `run_single_test`, one pytest process per file; `TEST_USE_PYTEST_BATCH` never set): GREEN. Each affected file passes in full standalone (test_world_logic 369, stale_guards 40, modal_integration 12, streaming_orchestrator 111, cowrite 6, god_mode_contract 30). 1 genuine pre-existing failure `test_full_lifecycle_walk_all_five_stages` (fails at base ef6c5e270c too — complete_finish_commit semantics, expected level 1 got 2).
- Design Doc Gate: was FAILing on Gate 0 — fixed by adding governing-doc `.md` into `## Tenets` via body edit. See [[design-doc-gate0-artifact-inside-tenets]].
- core-mvp-2 shard fail = pre-existing infra: `test_linux_default_runner_labels_for_container_workflows` FileNotFoundError on deleted `.github/workflows/mcp-smoke-tests.yml` (#7517 removed it) — NOT PR-4. See [[project_2026-06-13_green_gate_gate8_smoke_workflow_removed]].

**Cross-file test-isolation leak (non-blocking, CI-invisible):** Running a broad single-process `pytest -k "level_up or levelup"` flips 5 tests pass→fail (stale_guards x2, modal_integration routing x2, streaming x1) with `get_agent_for_input` returning LevelUpAgent for stale signals instead of StoryModeAgent. Passes at base, fails at HEAD → PR-4's added/reordered test files EXPOSE a pre-existing module-global leak in the routing/stale-guard path (agents.py — untouched by PR-4). CI per-file is immune; production unaffected (atomic reducer writes). Not a single identifiable polluter pair — needs full broad collection. Candidate follow-up: harden test isolation in the level-up suite.

Holdout eval is SEALED/operator-run — not executed here (see [[project_2026-06-13_levelup_v2_dark_factory_gate_pipeline]]).
