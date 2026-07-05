---
title: "PR #8162 partial fix vs canonical spec #7864 — don't ship narrow spell-slot fixes without consulting the spec"
type: source
tags: [worldarchitect.ai, spell-slots, ZFC, evidence, regression, learning]
date: 2026-07-05
source_file: feedback_2026-07-05_partial_spell_slot_fix_vs_canonical_spec.md
---

## Summary

On 2026-07-05, an agent shipped PR #8162 as a 2-file predicate widening (`mvp_site/game_state.py:reset_resource_registry_in_place` — `long_rest` now resets `short_rest` resources too) after only running `/advice` and reading tests. The user's stop-hook then surfaced that `/ms` and `/history` had been named in the goal but never run. Memory + slack-history search exposed the canonical spec at PR #7864 / `specs/2026-06-23-resource-registry-rest-tracking.md` (9 acceptance scenarios, 18 functional requirements, 8 open questions) and the user-validated closed design opinion in slack `1782275604.684449`: backend enforces 3 invariants (`clamp current ≥ 0`, `rest-reset on trigger match`, `session header auto-gen`); LLM owns mechanics and rules. Never hard-code Warlock / Ki / SuperiorityDice as backend predicates — those are open spec questions, not resolved.

## Key Claims

- The bug "long_rest doesn't recharge short_rest resources" is REAL but its canonical fix is a NEW `apply_short_rest_to_resources` helper alongside the existing `apply_long_rest_to_resources` — not a predicate widening inside `reset_resource_registry_in_place`.
- The 4-leg architecture (PR #7614, MERGED 2026-06-23): prompt MUST-emit rule + validator auto-fill `max` + custom-class canonical preservation + RED tests. The shipped fix skipped legs 1, 2, and 3.
- Warlock Pact Magic is a separate open spec question (slack `1782275604.684449`). It does NOT fit `resource_registry` (it's slot-level, has pact-specific scaling, no shared spellbook). Saying "long_rest resets short_rest" does not solve Pact Magic.
- Canonical evidence bundle: jleechantest twin on campaign `xK3fp5XrV24oarIINTF7` (or `n6PHTRPqDbSqvLAdLlEN` for #7613 baseline), in `evidence/repro-8160/REPRO.md` + capture script + pre/post Firestore snapshots. Unit tests are insufficient.
- Echo-reasoning TDD pattern: 25-RED-tests → 24-GREEN + 1-fix-needed; the single failing test is itself proof that the bug shape and the fix shape coexist (slack ts `1782279896.934079`, hermes, 2026-06-24).
- Test user = `jleechantest`, NOT `vnLp2G3m21PJL6kxcuAqmWSOtm73` (explicit user direction in the spec PR thread).

## Key Quotes

> "Recommend everything it should behave like real D&D but I don't really want hardcoded backend logic because the LLM should be able to design and create new resource systems maybe the LLM needs some type of registered resources thing in firestore and is the owner of the mechanics and rules but backend enforces the tracking. The LLM should see backend tracking and be able to override only during god mode" — jleechan, slack `1782275604.684449`, 2026-06-24

> "Keep going and fullrun if no more questions for this spellslot stuff thats expanded into general resource management" — jleechan, slack `1782279281.153619`

## Canonical artifacts

- **Canonical spec**: PR #7864 / `specs/2026-06-23-resource-registry-rest-tracking.md` (MERGED 2026-06-27)
- **4-leg canonical RED→GREEN fix**: PR #7614, commit `124902050f`, 2026-06-23
- **Backfill (closed-not-merged)**: PR #7862
- **Architectural precursor (closed)**: PR #7236
- **Open following PR (DO NOT land as-is)**: PR #8130 (15-file, +230/-102, prompt-collateral)
- **My partial fix being questioned**: PR #8162, commit `b4b5e84fab`, 2 files (+93/-5)
- **Canonical repro campaign ID**: `xK3fp5XrV24oarIINTF7` (or `n6PHTRPqDbSqvLAdLlEN` for #7613 baseline)
- **Test user**: `jleechantest`

## Connections

- [[SpellSlotFallback]] — concepts page covering the existing spell-slot fallback UX (different problem: empty `spells` array, not rest-reset)
- [[ZFC-Level-Up-Architecture]] — level-up modal architecture that this mechanic inherits from
- [[resource-rest-tracking-spec-2026-06-23]] — the canonical spec doc this PR should have aligned to
- [[ResourceRegistry]] (likely to be created) — the free-form registry dict + 3 invariants design
- [[WarlockPactMagic]] (likely to be created) — open-spec question; model-owned, NOT backend-hard-coded

## How to apply this lesson

1. BEFORE fixing any spell-slot-related bug in this repo, run `/ms "spell slot"` and `/history "spell slot"`, then read `specs/2026-06-23-resource-registry-rest-tracking.md` and scan slack #worldai threads `1781486145.366379` (master) + `1782269196.431339` (spec delivery).
2. If a fix doesn't address AT LEAST one of the 9 acceptance scenarios from #7864, do not ship.
3. Echo-reasoning TDD: write a test class where N-1 tests pass after the fix and 1 test fails showing the residual bug shape — that single failing test is itself proof the system has both healthy and corrupt code paths.
4. When the scope is genuinely narrower than the spec demands, file as **DRAFT** with `[SCOPE LIMIT]` prefix + an `XXX-spec-gap-filed-by` bead pointing at the missing sections. Never claim merge-ready when the canonical spec disagrees.
5. Test user = `jleechantest`. Campaign ID = `xK3fp5XrV24oarIINTF7` (or `n6PHTRPqDbSqvLAdLlEN` for #7613).
