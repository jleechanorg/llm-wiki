---
title: "Level-Up PR 6339 Verification Status 2026-04-17"
type: raw-note
tags: [worldarchitect-ai, level-up, pr6339, rewards-engine, stale-flags]
last_updated: 2026-04-17
---

# Level-Up PR 6339 Verification Status 2026-04-17

## Context

PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 (`feat/level-up-atomicity-v2`) is the current forward branch for the level-up bug-fix line after PR https://github.com/jleechanorg/worldarchitect.ai/pull/6276 merged the v4 rewards engine architecture incompletely. The design target remains the single-responsibility pipeline from `roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`: rewards and level-up canonicalization should centralize in `mvp_site/rewards_engine.py`, while `mvp_site/world_logic.py` should only adapt modal/UI surfaces that still need stateful context.

## Fresh PR and Branch Assessment

- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 is open with review changes requested and an unstable merge state.
- The original shared checkout was being moved by other agents, so verification moved to isolated worktree `/Users/jleechan/worldarchitect.ai/.worktrees/codex-level-up-6339-verify` on branch `codex/level-up-6339-verify`, based on PR #6339 head `24f9c910af898b211d4c0e58b245b2e33ea934d0`.
- Fresh remote PR state as of 2026-04-17:
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 remains the active local fix target. It was updated to commit `830081036a63d35286b064fe4f59c2b36cef55bf` without merging. GitHub still reports review `CHANGES_REQUESTED`; after the push its merge state is `DIRTY` and new checks are starting.
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6337 is a clean overlapping level-up planning-block preservation PR, but it is narrower than the PR #6339 local fix set and should not be treated as full confirmation.
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6350 is a draft recreation of superseded PR #6264 atomicity helpers; it is an architecture drift risk because it revives the line the single-responsibility design said to close.
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6349 and PR https://github.com/jleechanorg/worldarchitect.ai/pull/6346 are draft rewards-box/streaming recreations; they need reconciliation against rewards-engine-owned aliases and planning-block atomicity before review cycles continue.
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6336, PR https://github.com/jleechanorg/worldarchitect.ai/pull/6340, and PR https://github.com/jleechanorg/worldarchitect.ai/pull/6342 remain rewards/numeric-extraction related but are dirty or changes-requested.
  - PR https://github.com/jleechanorg/worldarchitect.ai/pull/6277 is still the benign RewardsBox TypedDict/schema-enforcement line and remains compatible with the PR #6339 direction.
- Open PR drift remains: older/world_logic-heavy PRs or recreations that push rewards fixes into `world_logic.py` are architecture risks if kept alive without rebasing onto the rewards-engine pipeline.

## Red Findings

- `mvp_site/tests/test_modal_integration.py` failed on PR #6339 because stale explicit false flags prevented routing to level-up, but `world_logic._inject_modal_finish_choice_if_needed` still injected level-up finish UI.
- `mvp_site/tests/test_end2end/test_rewards_agent_mechanical_end2end.py` failed because a mechanical RewardsAgent response could omit top-level `rewards_box`; `NarrativeResponse._validate_rewards_box()` also dropped fields produced by `rewards_engine.ensure_rewards_box()`.
- `mvp_site/tests/test_level_up_stale_flags.py` exposed two remaining stale/atomicity bugs: polling did not synthesize canonical top-level level-up UI from `game_state` when story fields were absent, and a stale `level_up_in_progress=True` flag could contaminate ordinary planning choices.

## Green Status

Local unit and end-to-end slices are green in the isolated worktree:

- `mvp_site/tests/test_level_up_stale_flags.py`: 66 passed.
- Rewards/modal/end-to-end slice: 99 passed, 1 skipped, 4 subtests passed.
- Targeted `world_logic` level-up/rewards slice: 82 passed, 1 skipped, 165 deselected, 8 subtests passed.
- Real local server plus real LLM strict level-up repro: 1/1 passed after red reproduction at `/tmp/worldarchitect.ai/codex_level-up-6339-verify/levelup_strict_repro/20260417_024259/iteration_001`.
- Real local server stale `level_up_pending` repro: 2/2 passed at `/tmp/worldarchitect.ai/codex_level-up-6339-verify/stale_level_up_pending_repro/iteration_002`.
- Real local server streaming level-up E2E: 2/2 passed at `/tmp/worldarchitect.ai/codex_level-up-6339-verify/level_up_streaming_e2e/iteration_001`.

Implementation direction:

- Align `agents.get_agent_for_input()` stale pending logic with canonical `rewards_engine.resolve_level_up_signal()`.
- Preserve rewards-engine-owned fields through `NarrativeResponse._validate_rewards_box()`.
- Make `rewards_engine.ensure_rewards_box()` emit schema-compatible aliases (`current_xp`, `xp_total`, `new_level`, `next_level_xp`, `progress_percent`) while retaining canonical fields.
- Add a canonical UI-pair resolver in `world_logic.py` only for the stateful polling/modal wrapper responsibilities still owned there.

## Remaining Work

- No merge should happen until the GitHub review state and PR gates are resolved.
- No PR should be merged during this verification pass.
- Ruff on the touched file set still reports pre-existing style warnings in `mvp_site/narrative_response_schema.py` and old `mvp_site/world_logic.py` sections; the new patch-introduced warnings were cleaned.

## Connections

- [[PR6339]]
- [[LevelUpVerificationStatus]]
- [[RewardsEngine]]
- [[LevelUpCodeArchitecture]]
- [[LevelUpStaleFlagGuards]]
