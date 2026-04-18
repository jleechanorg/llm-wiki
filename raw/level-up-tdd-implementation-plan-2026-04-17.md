# Level-Up Integrated Fix TDD Implementation Plan

**Date:** 2026-04-17
**Canonical source:** `/Users/jleechan/roadmap/2026-04-17-level-up-tdd-implementation-plan.md`
**Repository:** `/Users/jleechan/worldarchitect.ai`
**Primary beads:** `rev-k330`, `rev-dcpn`, `rev-6hym`

## Raw Ingest Note

This raw wiki ingest records the full implementation contract from the canonical roadmap plan. The roadmap file remains the source of operational truth for AO workers; this raw file preserves the same decisions in the wiki corpus.

## Executive Decision

Create one clean replacement PR from `origin/main` for the non-autor level-up bug-fix line. Do not reopen PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339 as-is, and do not merge PR https://github.com/jleechanorg/worldarchitect.ai/pull/6351 as-is.

Recommended clean branch: `fix/level-up-rewards-integrated-main`.

The replacement PR should port only proven behavior from the related PRs, keep implementation ownership explicit, and prove the result with RED/GREEN tests, real local server, real LLM integration runs, and video evidence where UI/browser behavior is claimed.

## Source Truth

Binding context:

- `/Users/jleechan/roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`
- `/Users/jleechan/roadmap/level-xp-centralization-design-2026-04-13.md`
- `/Users/jleechan/roadmap/2026-04-17-level-up-centralization-learning.md`
- `/Users/jleechan/roadmap/2026-04-17-level-up-pr-disposition-plan.md`
- `/Users/jleechan/llm_wiki/wiki/sources/level-up-pr-drift-root-cause-harness-2026-04-17.md`
- `/Users/jleechan/llm_wiki/wiki/sources/level-up-atomicity-root-cause-2026-04-17.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/BehavioralEquivalenceAudit.md`
- `/Users/jleechan/llm_wiki/wiki/concepts/LevelUpVerificationStatus.md`

Important interpretation:

- The v4 single-responsibility design is the target direction, not proof that old behavior is safely replaceable.
- `world_logic.py` full stripping to about 1500 lines was tombstoned as written after the behavioral audit.
- `world_logic.py` may still own narrow modal/state recovery projection until equivalent behavior exists in `rewards_engine.py`.
- Any `world_logic.py` change must include an exception statement explaining why it is modal/state recovery and not misplaced rewards computation.

## Related PR Inputs

- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6339: reference only for XP-driven atomicity, stale explicit-false guards, canonicalizer planning-block preservation, and real `testing_mcp` proof.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6336: source ideas only for `rewards_engine.py` visibility, gold/loot visibility, and stale choice cleanup.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6277: clean schema groundwork candidate; fold only if needed for the integrated fix.
- PR https://github.com/jleechanorg/worldarchitect.ai/pull/6351: current WIP port attempt, but not a merge vehicle unless cleaned, unstacked, reviewed, and re-proven.

Ignore autor-tagged/titled PRs for merge disposition unless Jeffrey explicitly promotes one into this bug-fix line.

## Commit Discipline

1. Commit 1 is RED tests only. Add failing tests that reproduce the bugs against clean `origin/main`. No production-code changes.
2. Commit 2+ is GREEN production code only. Minimal code that makes the RED tests pass. Do not add or rewrite tests in the same commit unless explicitly justified.
3. Commit 3+ is evidence harness/docs only. Evidence scripts, captured artifact references, PR body updates, and wiki/roadmap references. Do not mix code fixes into evidence commits.

## Behavioral Contract

The clean PR must prove:

- Pre-level-up XP progress emits progress-only rewards data when appropriate without requiring a level-up planning block.
- XP-driven threshold crossing preserves the level-up UI even when explicit level-up flags are absent.
- Explicit `level_up_in_progress=False` blocks stale reactivation unless a stronger active signal exists.
- Explicit `level_up_pending=False` blocks stale reactivation unless in-progress is true.
- `level_up_complete=True` with missing `rewards_box` can synthesize the required UI without off-by-one target-level errors.
- Active level-up UI preserves atomic `rewards_box` plus valid `planning_block` choices.
- Inactive level-up UI scrubs stale choices such as `complete_levelup`, `finish_level_up_return_to_game`, and stale ASI choices.
- Gold, loot, and XP-progress-only rewards remain visible when no level-up planning block is required.
- Malformed or non-standard LLM `rewards_box` payloads are normalized before persistence and rendering.
- Streaming and non-streaming paths persist equivalent structured fields for equivalent LLM output and state transitions.

## Ownership Rules

- `game_state.py`: XP math, Firestore state reads/writes, raw persisted flags, `LevelProgressionState`.
- `rewards_engine.py`: rewards/progression decisions, rewards-box construction, normalization, visibility, stale choice cleanup where it can be pure.
- `world_logic.py`: modal/story adapter, stateful projection from persisted story/game state, modal finish-choice injection, living-world and non-rewards planning assembly.
- `streaming_orchestrator.py` or `llm_parser.py`: orchestration and persistence path; no independent rewards decisions.
- Frontend files: render server-decided payloads; no duplicated level-up visibility logic.

Before deleting or redirecting old logic, write a behavioral-equivalence table that compares old and new outputs for representative states.

## Four-Layer TDD Plan

### Layer 1: Unit RED

Primary test targets:

- `/Users/jleechan/worldarchitect.ai/mvp_site/tests/test_rewards_engine.py`
- `/Users/jleechan/worldarchitect.ai/mvp_site/tests/test_level_up_stale_flags.py`
- `/Users/jleechan/worldarchitect.ai/mvp_site/tests/test_world_logic.py`
- `/Users/jleechan/worldarchitect.ai/mvp_site/tests/test_mcp_protocol_end2end.py`

Required RED cases:

- XP-driven level-up signal preserves `rewards_box` and `planning_block`.
- Canonicalizer does not wipe an already-injected valid level-up `planning_block`.
- Explicit false stale flags block stale modal resurrection.
- Gold/loot/progress-only rewards do not require level-up choices.
- List-format and dict-format `planning_block.choices` both normalize in diagnostics/tests.
- `NarrativeResponse` or equivalent schema preservation keeps canonical `rewards_box` fields.

### Layer 2: Backend End-to-End RED/GREEN

Required checks:

- Same action/state shape produces equivalent rewards/planning structured fields in stream and non-stream paths where available.
- Persisted story entry includes normalized `rewards_box` fields.
- Post-finish state does not leave `rewards_pending.level_up_available` stuck.

### Layer 3: Real Local Server + Real LLM MCP

Mandatory before claiming the level-up bugs are fixed. Use real services and no mock-mode paths:

```bash
cd /Users/jleechan/worldarchitect.ai
env -u MCP_TEST_MODE -u MOCK_SERVICES_MODE -u USE_MOCK_SERVICES \
  TESTING_AUTH_BYPASS=true \
  GOOGLE_APPLICATION_CREDENTIALS=/Users/jleechan/serviceAccountKey.json \
  ./vpython mvp_site/main.py serve
```

Canonical direct script runs:

```bash
cd /Users/jleechan/worldarchitect.ai/testing_mcp
../vpython test_levelup_strict_repro.py --server http://127.0.0.1:8001
../vpython test_stale_level_up_pending_repro.py --server http://127.0.0.1:8001
../vpython streaming/test_level_up_streaming_e2e.py --server http://127.0.0.1:8001
```

### Layer 4: Browser/UI Real Server + Video

Mandatory for any browser level-up modal, rewards box, or planning choices claim. Video evidence must show URL and git SHA context, before state, triggering user action, after state, and captioned RED/GREEN runs when UI behavior is fixed. Screenshots alone are insufficient.

## Evidence Bundle Standard

Each RED and GREEN run writes an evidence bundle under:

```text
/tmp/worldarchitect.ai/level-up-integrated/<phase>/<layer>/
```

Required files include `run.json`, `metadata.json`, `evidence.md`, `methodology.md`, `README.md`, `request_responses.jsonl` for API/MCP/LLM work, checksums, terminal/tmux video for evidence-bearing terminal runs, and UI/browser video for Layer 4.

## AO Worker Split

- Worker A: RED Unit And Backend Tests. Tests only. No production code.
- Worker B: Production Fix Port. Production files only. Wait for or import Worker A's RED contract before claiming GREEN.
- Worker C: Layer 3 Real MCP Harness Evidence. `testing_mcp/` and `/tmp/worldarchitect.ai/level-up-integrated/` only. No production code. No mock toggles.
- Worker D: Layer 4 Browser/UI Video Evidence. `testing_ui/` and `/tmp/worldarchitect.ai/level-up-integrated/` only. No production code.
- Worker E: Skeptic / Drift Guard. Read-only by default. Verify no drift from the plan.

## Merge Readiness

Do not merge until RED tests exist and fail against pre-fix code, GREEN code is separated, Layer 1 and Layer 2 pass, Layer 3 real local server plus real LLM runs pass, Layer 4 video exists for UI claims, the PR evidence bundle has separate RED/GREEN artifacts, and 7-green verification reads actual gate logs.
