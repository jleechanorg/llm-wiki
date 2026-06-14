---
name: pr
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: c3c948a5-d372-4f31-88d7-1a9eb5a2f2d6
---

PR #7268 (level-up clean-flags refactor, branch `delete-stale-level-flags`, head `ddfd4f10`, repo jleechanorg/worldarchitect.ai). Deletes stale `level_up_pending`/`level_up_in_progress`/`level_up_complete`/`level_up_cancelled` lifecycle flags; routes modal from derived state (canonical `level_up_signal`, `target_level > current_level`). **Net production LOC +553** (additive refactor, not pure deletion).

**Status 2026-06-07:** CodeRabbit **APPROVED** (22:38Z), `mergeable=MERGEABLE`, reviewDecision empty. **Remaining hard blocker: 2 Directory tests failing** (core-mvp-1/2 self-hosted) → Green Gate ([rev-jyeff]). Merge human-gated.

This session: rewrote PR body template-compliant with per-file `Before→Now→Why` for all 19 non-test files; net-additions audit = **no new boolean lifecycle flags** (new `level_up_in_progress`/`level_up_pending` are read-only derived `@property` shims) and **no tenet violations** (XP is display-only hydration, never primary). **Replied to all 12 author inline comments #10–21** (commit had predated the review by 40 min).

**Queued followups (beads):**
- [rev-1c98x] P1 — REMOVE god-mode HP-alias mirroring (`_mirror_top_level_player_health_aliases_in_place` + `prefer_top_level_health_aliases` + `agent_mode` threading on `validate_and_correct_state`, ~90 LOC in game_state.py). It is NEW, unrelated to flag deletion (scope creep), AND an RCF violation (backend reconciliation of two schema-sanctioned HP homes; root cause = schema 2 HP fields + god_mode prompt writes only legacy `hp_current`). Fix prompt-first in a separate HP-consolidation PR. Maps author comments #11/12/13.
- [rev-x2sja] P1 — prompt fix: `level_up_now` entry choice `text` MUST begin with "Level Up". Root cause confirmed: `level_up_instruction.md:115-117` only soft-examples the label ("visible labels like 'Level Up to Level N'"); no hard rule. HISTORICAL RED ARTIFACT in source `fdpDipUzknuchYPIHtgA`: id=`level_up_now` text="Meditate on your Oath (Level Up)". Evidence `/tmp/worldarchitect.ai/repro-exports/pr7268_levelup_choice_wording/VERDICT.md`.
- [rev-15i5c] P2 — in-place cleanups: `llm_parser._read_level_up_flag` dead branch (both arms set False); `rewards_engine` XP-key dedup (`_XP_GAINED_KEYS`/`_XP_TO_NEXT_KEYS`); `_is_stdlib_test_double` unittest.mock guard in prod.
- [rev-naxbs] P2 — Bugbot: `GameState.__init__` should also strip `level_up_stage`/`pending_level_up_selections` (else stripped `level_up_complete` leaves orphan scratch that re-derives active modal; narrow legacy-save edge case).

**PR #7337 (separate) — DO NOT MERGE:** skeptic VERDICT FAIL — `_resolve_level_up_from_rewards_box` accepts stale prior-level thresholds (level=4/xp=3000/next_level_xp=2700 → manufactures level-5) ([rev-t3vjp]); ZFC concern re-derives from rewards_box XP instead of canonical `level_up_signal` ([rev-hrd9i]); file-overlap with #7268 on `rewards_engine.py` needs sequencing ([rev-je2bt]).

See [[feedback_2026-06-07_copy_campaign_dest_default_footgun]] for the repro-tooling footgun. Nextsteps doc: `roadmap/nextsteps-2026-06-07-pr7268-cleanup-and-followups.md`.
