---
name: Stuck LevelUpAgent — clearing mechanism already on main, evaded by in_progress=true
description: is_stale_level_up_pending exists+wired on main; stuck L20 case is the deliberate level_up_in_progress=true early-return; no open PR is a proven fix
type: project
bead: rev-vcd2u
---

Answer to "would one of these open PRs fix the stuck LevelUpAgent?": **No open PR is a proven net-new fix.**

The stale-flag clearing mechanism already exists on `main` and is already wired:
- `mvp_site/rewards_engine.py:1430` — `def is_stale_level_up_pending(game_state_like)`
- `mvp_site/agents.py:3352` — `... and not rewards_engine.is_stale_level_up_pending(game_state)` in routing

Why the L20 campaign stays stuck anyway — the early-return gate at `rewards_engine.py:1441-1452`:
`if (not level_up_pending_flag or level_up_in_progress_flag or rewards_transition_actionable): return False`
When `level_up_in_progress=true` (active god-mode/level-up planning block) the detector returns False = "not stale" = agent stays engaged, by design (never abort an in-flight level-up). Stuck case = `level_up_pending=true` AND `level_up_in_progress=true`. Complement of bead [[rev-y9o32]] (in_progress=false → finish routes to RewardsAgent, level never commits 15→16).

Per-PR: #7239 (prompt consolidation) = emission/skip/surfacing only, cannot clear a Firestore-persisted flag. #7199 carries Bug A level merge-back (candidate root, UNPROVEN). #7221/#7214 refine logic that already exists. #7194 (daily GCP level_up_organic harness) is the keystone repro gate, not a fix — [[rev-rmhpl]].

RCF proof (2026-06-03): Bug B refuted (already canonicalized game_state.py:824-873); Bug A unproven (campaign hit L20 max, no clean repro).

Live merge state 2026-06-04: #7155 MERGED 03:55Z; #7239 flipped CONFLICTING→MERGEABLE (CHANGES_REQUESTED); #7171/#7194/#7199 OPEN+MERGEABLE. Order: #7171 → #7239 (close #7235) → #7194 → backend ONLY after #7194 proves Bug A.

**Why:** Prevents the recurring false claim that a prompt PR "fixes the stuck agent" — it can't touch persisted flags — and stops speculative backend enforcement that CLAUDE.md forbids without a repro + human approval.

**How to apply:** When asked whether a level-up PR clears a stuck LevelUpAgent: check `is_stale_level_up_pending` gate (`rewards_engine.py:1441-1452`) and the `level_up_in_progress` flag first; require #7194's repro before endorsing any backend fix; register any backend correction in `backend_adjustment_specs.py` with explicit in-thread human approval.
