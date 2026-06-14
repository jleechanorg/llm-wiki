# PR 5 routing migration — rebased onto PR 5.5 (2026-06-08)

PR #7377 rebased onto PR 5.5 head `e5a5d5a0b1` per new chain order
PR 1 → 2 → 3 → 4 → 5.5 → 5 → 6.

- **PR**: https://github.com/jleechanorg/worldarchitect.ai/pull/7377
- **Old SHA**: 057e453435 (PR 3 base)
- **New SHA**: ecf279618b (PR 5.5 base, force-with-lease per user approval)
- **Commit prefix**: `[antig] level-up: route from canonical session status (PR 5, rev-pctz8.5)`
- **Base branch**: feature/level-up-session-pr5-5 (changed via `gh pr edit --base`, did not need to close PR)
- **Test result**: 992 passed, 12 skipped, 130 subtests passed in 5.54s (0 regressions)

## What landed
- 6 switch points in `mvp_site/agents.py` route from canonical `level_up_session.status` (LevelUpAgent matches, CharacterCreationAgent drops escape hatch, get_agent_for_input drops legacy fields, duplicate escape collapsed, rewards-to-level-up uses status, world_logic modal-lock/finish/time-freeze/modal-entry use adapters)
- 5 read-side routing adapters in `mvp_site/level_up_session.py` (`_coerce_level_up_session`, `get_session_status`, `should_route_to_level_up_agent`, `is_level_up_routing_terminal`, `is_level_up_modal_active`) — mutator state machine UNCHANGED
- 24 new tests in `mvp_site/tests/test_level_up_session_routing_adapters.py`
- Updates to test_agents.py, test_modal_base.py, test_modal_integration.py, test_modal_routing_fixtures.py, test_rewards_engine.py, test_world_logic.py, test_world_logic_modal_coverage.py

## Lessons
- **Rebase after push requires force-with-lease — ASK first.** The directive's "first push to new remote, NOT a force-push" was ambiguous; rebase + force-push is the standard flow and the user approved --force-with-lease once the conflict was named explicitly. Future directives should specify rebase-force strategy upfront.
- **0 file overlap between PR 5 and PR 5.5** (verified via `git diff --name-only` + `comm -12`); rebase was a clean fast-forward replay of one commit. The 4 PR 5.5 commits added new files only (`level_up_session_observability.py`, new tests, new script) plus `rewards_engine.py` edits.
- **PR 5.5 also modified `mvp_site/level_up_session.py`** (commit `55782df35b fix(level_up_session): gate reducer on canonical_signal to prevent phantom sessions`). My commit also modified that file. No conflict because we touched different lines (PR 5.5 added a `canonical_signal` gate, I added read-side adapters).
- **`gh pr edit --base <new-base>` works to retarget an open PR's base branch** without needing to close and reopen.
- **7-file pytest directive** (routing_adapters + agents + modal_integration + modal_routing_fixtures + world_logic + rewards_engine + level_up_stale_guards) catches all 6 switch points + the routing-adapter API surface in one run.
- **CI green gates**: lint, type-check, test, coverage, design-doc-grep, schema-coverage, test-deployment-build all SUCCESS. Green Gate + Directory tests still in-flight (unknown). No FAIL/ERROR.
- **PR #7374 (PR 5.5) is at head `55782df35b`** but it is itself based on PR 3 head `263ff6e2d2` (not main) — so PR 5 must base on the PR 5.5 BRANCH tip, not on PR 5.5's merge to main (which doesn't exist yet).
