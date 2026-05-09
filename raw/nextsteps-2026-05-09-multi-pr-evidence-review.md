# Nextsteps — Multi-PR Evidence & Review Block — 2026-05-09

## Table of contents

- [Executive summary](#executive-summary)
- [Context](#context)
- [Bead index](#bead-index)
- [Work queue](#work-queue)
- [PR / merge state](#pr--merge-state)
- [Learnings pointer](#learnings-pointer)
- [Roadmap pointer](#roadmap-pointer)

## Executive summary

- **12 open PRs reviewed and augmented** — Deep-diff analysis + /es-level test additions across 7 production PRs (2,348 new LOC of Layer 2-3 test code); 2 PRs (#6841, #6833) required no additions (existing coverage / docs-only).
- **3 new PRs emerged during session** — #6844 (stale combat state loop), #6845 (harness guardrails), #6846 (runner self-healing) — all untested for /es compliance yet.
- **Root cause trends identified** — Trend A (admin override state poisoning), Trend B (modal intersection neglect), Trend C (refactoring friction/duplication). Highest-impact fix: `ADMIN_OVERRIDE_CONTRACTS` dict + `_validate_post_override_state()`.
- **Manual test campaign cloned** — `Alexiel V2` → `jleechantest@gmail.com`, campaign ID `C4XU4SgvzbpvuZQi8uCs` for hands-on verification.
- **No PRs merged yet** — All 12 PRs remain OPEN, none have review approvals. Layer 3 MCP tests need real server with `WORLDAI_DEV_MODE=true` to produce publishable /es evidence.
- Beads: [rev-admin-contract](#) (to be created), [rev-modal-intersect](#) (to be created), [rev-bindthis-eslint](#) (to be created)

## Context

Session starting from origin/main HEAD `e8a3c385f` covered: (1) diff analysis for all open PRs, (2) /es-compliant test additions to 7 PR branches, (3) root cause analysis of recurring bug classes across PR diffs, (4) manual test campaign cloning, (5) /nextsteps situational assessment. The session scoped itself to adding evidence-grade tests, not to merging or to running live server tests (which need `WORLDAI_DEV_MODE=true` + real Firebase credentials).

### Test additions by PR

| PR | Branch | Test file(s) | Layer | Count | Status |
|---|---|---|---|---|---|
| [#6843](https://github.com/jleechanorg/worldarchitect.ai/pull/6843) | `fix/location-progress-mapping` | `mvp_site/tests/test_preventive_guards.py` (extended) | L1 | 9 | 9/9 PASS |
| [#6842](https://github.com/jleechanorg/worldarchitect.ai/pull/6842) | `dev1778308837` | `testing_mcp/core/test_godmode_cc_modal_exit_real_e2e.py` | L3 | 3 | Import verified, needs live server |
| [#6840](https://github.com/jleechanorg/worldarchitect.ai/pull/6840) | `investigate-gcp-latency` | `testing_mcp/test_compact_json_streaming_contract.py`, `test_cache_async_streaming_flow.py` | L3 | 2 suites | Import verified, needs live server |
| [#6839](https://github.com/jleechanorg/worldarchitect.ai/pull/6839) | `fix/turn-scoped-cooldown-clear` | `mvp_site/tests/test_end2end/test_non_streaming_cooldown_strip_end2end.py` | L2 | 5 | 5/5 PASS |
| [#6821](https://github.com/jleechanorg/worldarchitect.ai/pull/6821) | `feature/llm-defined-xp-thresholds` | `testing_mcp/test_llm_defined_xp_thresholds_real_e2e.py` | L3 | 3 | Import verified, needs live server |
| [#6779](https://github.com/jleechanorg/worldarchitect.ai/pull/6779) | `feat/campaign-wizard-base` | `testing_mcp/test_campaign_wizard_real_e2e.py` | L3 | 3 | Import verified, needs live server |
| [#6825](https://github.com/jleechanorg/worldarchitect.ai/pull/6825) | `worktree_quality` | `testing_mcp/test_core_memory_compaction_e2e.py` (rewrite) | L3 | 3 | Import verified, needs live server |

### Root cause trends

**Trend A — Admin override state poisoning**: God mode and admin actions short-circuit state machines (character creation, level-up, combat), leaving stale flags. Fix: `ADMIN_OVERRIDE_CONTRACTS` dict mapping each override action to its required post-override invariants, enforced by `_validate_post_override_state()`.

**Trend B — Modal intersection neglect**: When two modal systems interact (CC + level-up, combat + LW), neither handler clears the other's stale state. Fix: modal intersection property tests (hypothesis-style parametrized).

**Trend C — Refactoring friction/duplication**: Living world trigger processing has parallel code paths in `world_logic.py` and `living_world_contract.py`. JS event handlers use `.bind(this)` which breaks `removeEventListener`. Fix: cross-file reference lint + ESLint rule banning `.bind(this)` in addEventListener/removeEventListener pairs.

## Bead index

| Bead | Title | Status | Link |
|------|-------|--------|------|
| rev-admin-contract | Admin override state contract — ADMIN_OVERRIDE_CONTRACTS dict + post-override validation | to be created | — |
| rev-modal-intersect | Modal intersection property tests (CC + level-up, combat + LW) | to be created | — |
| rev-bindthis-eslint | ESLint rule banning .bind(this) in addEventListener/removeEventListener pairs | to be created | — |
| rev-pygku | PR 6825: fix test_active_modal_stale_transition_signal | closed | `br show rev-pygku` |
| rev-75ld8 | Design natural Alexiel copied-campaign core-memory proof | open | `br show rev-75ld8` |
| rev-o46gn | Prove live core-memory quality after prompt contract | open | `br show rev-o46gn` |
| rev-a0ezb | PR 6800: Gate 6 evidence stale — re-run /es required | open | `br show rev-a0ezb` |
| rev-k46g8 | PR 6834: repair evidence publication claims and close proof gaps | open | `br show rev-k46g8` |

## Work queue

### 1. Run Layer 3 MCP tests against live server for /es evidence (HIGH)

**Goal**: Produce publishable /es evidence bundles for PRs #6842, #6840, #6821, #6779, #6825 by running their Layer 3 MCP tests against a real local server.

**Prerequisites**: `WORLDAI_DEV_MODE=true`, `WORLDAI_GOOGLE_APPLICATION_CREDENTIALS=~/serviceAccountKey.json`, Flask server running.

**Acceptance criteria**: Each PR has at least one evidence bundle with `metadata.json.git_head` matching branch HEAD, test output showing PASS, and gist linked in PR body.

**Dependencies**: Real server + Firebase credentials must be active.

**Tracks**: [rev-a0ezb](br show rev-a0ezb), [rev-o46gn](br show rev-o46gn)

### 2. Implement ADMIN_OVERRIDE_CONTRACTS + _validate_post_override_state() (HIGH)

**Goal**: Create a declarative contract dict mapping each admin/god-mode override action to the invariants it must establish post-execution. Add `_validate_post_override_state()` to `world_logic.py` or new `admin_contracts.py`.

**Example**:
```python
ADMIN_OVERRIDE_CONTRACTS = {
    "god_mode_level_up": {
        "clear_flags": ["level_up_pending", "level_up_in_progress"],
        "assert_game_state": {"level": "target_level"},
    },
    "god_mode_character_creation": {
        "clear_flags": ["character_creation_in_progress"],
        "assert_game_state": {"character_creation_stage": None},
    },
    "admin_combat_reset": {
        "clear_flags": ["combat_active"],
        "assert_game_state": {"combat_state": None},
    },
}
```

**Files**: `mvp_site/world_logic.py` (primary), `mvp_site/admin_contracts.py` (new if needed), `mvp_site/tests/test_admin_override_contracts.py`

**Acceptance criteria**: Every admin override path in `world_logic.py` calls `_validate_post_override_state()` after mutation; unit tests prove stale flags are caught.

**Tracks**: [rev-admin-contract](#)

### 3. Add modal intersection property tests (MEDIUM)

**Goal**: Hypothesis-style parametrized tests that verify combinations of modal states don't leave stale artifacts.

**Scenarios to cover**:
- CC active + level-up trigger → CC cleared, level-up entered correctly
- Combat active + living world turn → combat state preserved, LW events processed
- Level-up active + combat trigger → level-up modal preserved, combat queued

**Files**: `mvp_site/tests/test_modal_intersection_properties.py` (new)

**Acceptance criteria**: Tests pass for all 3+ intersection combos; failure proves at least one stale-flag bug.

**Tracks**: [rev-modal-intersect](#)

### 4. Add ESLint rule for .bind(this) event listener pattern (MEDIUM)

**Goal**: Prevent PR #6841 class of bug (addEventListener with `.bind(this)` makes removeEventListener fail silently).

**Files**: `mvp_site/frontend_v1/.eslintrc.json` or custom rule, `mvp_site/tests/frontend/test_eslint_bind_this.js`

**Acceptance criteria**: `eslint mvp_site/frontend_v1/js/` flags `.bind(this)` inside `addEventListener`/`removeEventListener` call pairs.

**Tracks**: [rev-bindthis-eslint](#)

### 5. Add /es evidence to 3 new PRs #6844, #6845, #6846 (MEDIUM)

**Goal**: These PRs were opened during the session and have no /es-compliant tests:
- #6844 (stale combat state loop) — needs a Layer 2-3 test proving the combat-state-clear fix
- #6845 (harness guardrails) — docs-only, may be N/A
- #6846 (runner self-healing) — CI/infra, may be N/A

**Files**: TBD per PR diff analysis

**Acceptance criteria**: Each PR with production `mvp_site/**` changes has at least one Layer 2+ test.

### 6. Manual validation of cloned campaign (LOW — user action)

**Goal**: User logs in as `jleechantest@gmail.com`, opens campaign `C4XU4SgvzbpvuZQi8uCs`, exercises rewards/level-up flow.

**Campaign details**: Source `71OJ7qE0VDcOuUbgInSH` (Alexiel V2, 412 entries), cloned via `scripts/copy_campaign.py`. Firebase UID `0wf6sCREyLcgynidU5LjyZEfm7D2`.

**Acceptance criteria**: No spurious modals, stale signals, or combat loops during normal play.

### 7. Get CR approvals for all open PRs (HIGH — external dependency)

**Goal**: All 12 open PRs need `reviewDecision: APPROVED` before merge.

**Current state**: All 12 PRs have `reviewDecision: ""` (pending). None have human or CodeRabbit approval.

**Acceptance criteria**: `gh pr view <n> --json reviewDecision --jq .reviewDecision` returns `APPROVED`.

**Dependencies**: External — reviewers must approve.

## PR / merge state

| PR | Branch | State | Tests Added | /es Status |
|---|---|---|---|---|
| [#6846](https://github.com/jleechanorg/worldarchitect.ai/pull/6846) | `fix-runner-self-healing` | OPEN | none yet | needs assessment |
| [#6845](https://github.com/jleechanorg/worldarchitect.ai/pull/6845) | `chore/harness-guardrails` | OPEN | none yet | docs-only, likely N/A |
| [#6844](https://github.com/jleechanorg/worldarchitect.ai/pull/6844) | `worktree_agent_wrong` | OPEN | none yet | needs Layer 2-3 test |
| [#6843](https://github.com/jleechanorg/worldarchitect.ai/pull/6843) | `fix/location-progress-mapping` | OPEN | L1 (9 PASS) | needs L3 live-server run |
| [#6842](https://github.com/jleechanorg/worldarchitect.ai/pull/6842) | `dev1778308837` | OPEN | L3 (3 tests) | needs live-server run |
| [#6841](https://github.com/jleechanorg/worldarchitect.ai/pull/6841) | `fix-ui-campaign-issues-20260508` | OPEN | existing L5 browser | sufficient |
| [#6840](https://github.com/jleechanorg/worldarchitect.ai/pull/6840) | `investigate-gcp-latency` | OPEN | L3 (2 suites) | needs live-server run |
| [#6839](https://github.com/jleechanorg/worldarchitect.ai/pull/6839) | `fix/turn-scoped-cooldown-clear` | OPEN | L2 (5 PASS) | needs L3 live-server run |
| [#6833](https://github.com/jleechanorg/worldarchitect.ai/pull/6833) | `docs/gemini-merge-guard` | OPEN | none (docs-only) | N/A |
| [#6825](https://github.com/jleechanorg/worldarchitect.ai/pull/6825) | `worktree_quality` | OPEN | L3 (3 tests) | needs live-server run |
| [#6821](https://github.com/jleechanorg/worldarchitect.ai/pull/6821) | `feature/llm-defined-xp-thresholds` | OPEN | L3 (3 tests) | needs live-server run |
| [#6779](https://github.com/jleechanorg/worldarchitect.ai/pull/6779) | `feat/campaign-wizard-base` | OPEN | L3 (3 tests) | needs live-server run |

## Learnings pointer

- `~/roadmap/learnings-2026-05.md` — new sections `2026-05-09 — Admin override state poisoning trend` and `2026-05-09 — Modal intersection neglect pattern`

## Roadmap pointer

- Updated `roadmap/README.md` — Recent activity (rolling)
