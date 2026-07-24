---
title: "Resource Rest-Tracking Spec (PR #7864, 2026-06-23)"
type: concept
tags: [worldarchitect.ai, spell-slots, resource-registry, ZFC, design-spec]
date: 2026-07-05
---

## Problem

Spell-slot and general-resource consumption is the D&D 5e mechanic where the model emits `state_updates.player_character_data.resources.<resource>.<level>.current -= 1` (or similar) when a player casts a spell or uses a class feature. As of 2026-06, the system had **5 distinct broken layers**:

1. LLM MUST-emit rule compliance 34.4% (model skipped the resource tracking on most turns)
2. `_deep_merge` accepted partial deltas without enforcing `max`
3. `apply_long_rest_to_resources` existed and was unit-tested but **NEVER CALLED in production merge path** (`validate_game_state_updates` in `mvp_site/world_logic.py:5180`)
4. No `apply_short_rest_to_resources` helper existed
5. The other-resources validator was untyped

## Closed design decisions

Per slack `1782275604.684449` (jleechan, 2026-06-24):

> "Recommend everything it should behave like real D&D but I don't really want hardcoded backend logic because the LLM should be able to design and create new resource systems maybe the LLM needs some type of registered resources thing in firestore and is the owner of the mechanics and rules but backend enforces the tracking."

**Backend enforces 3 invariants**:
1. `clamp current ≥ 0` (never negative)
2. `rest-reset on trigger match` (long_rest + short_rest)
3. `session header auto-gen` (display state)

**LLM owns**: mechanics, rules, resource definitions, god-mode override capability.

## Architecture

- `resource_registry`: free-form dict on `player_character_data.resource_registry`, keyed by resource id (e.g. `warlock_spell_slots`, `monk_ki_points`).
- Each entry has: `display_name`, `current`, `max`, `reset_trigger` ∈ {`None`, `long_rest`, `short_rest`}, `category` ∈ free-form (e.g. `spell_slot`, `class_feature`, `ability`, `consumable`).
- `mvp_site/game_state.py:GameState.reset_resources(trigger)` — high-level wrapper.
- `mvp_site/firestore_service.py:_apply_rest_resource_reset(state_to_update, trigger)` — production wire path, called from `update_state_with_changes` when `rest_taken` field is present in LLM-emitted `state_updates`.
- `apply_long_rest_to_resources(resources, world_time)` — Firestore-level helper, unit-tested but originally not on the production wire path.

## 9 acceptance scenarios (from PR #7864 spec)

(outline — see `/Users/jleechan/.worktrees/worldarchitect/wa-3064/specs/2026-06-23-resource-registry-rest-tracking.md` for the full 18-functional-requirement detail)

## 8 open stakeholder questions (from PR #7864 spec)

- NPC rest scope: do companions get the same reset?
- Non-emit fallback: when the model skips the `current` delta, do we clamp, leave alone, or auto-derive?
- Delta-vs-absolute semantics: `current -= 1` vs `current = N`
- Future timestamps: roll forward vs reject on stale `last_long_rest_world_time`
- Class-specific short rest: Arcane Recovery (Wizard), Natural Recovery (Druid), Bardic Inspiration refresh
- Warlock Pact Magic: separate resource class vs modeled inside `resource_registry`
- Hit dice: track in `resources.hit_dice` or own dict
- Custom trigger types: user-defined beyond long_rest/short_rest

## 4-leg canonical fix (PR #7614, MERGED 2026-06-23)

1. Prompt MUST-emit rule — explicit instruction at top of `game_state_instruction.md`
2. Validator auto-fill `max` — `_canonicalize_resource_registry_in_place` (preserves existing numbers, fills missing `max` from `current`)
3. Custom-class canonical preservation — Warlock pact magic preserved through transform
4. RED tests — 25 cases exercising (1)-(3) on canonical Tenebria campaign `FsiyESY987DF2lfgolCI`

## Echo-reasoning TDD pattern

25 RED tests → 24 GREEN + 1 fix-needed. The single failing test is itself proof that the bug shape and the fix shape coexist in the same test class. NOT a unit-only "before/after" diff.

## Canonical evidence

- Campaign ID: `xK3fp5XrV24oarIINTF7` (general); `FsiyESY987DF2lfgolCI` (original #7613); `n6PHTRPqDbSqvLAdLlEN` (jleechantest twin)
- Test user: `jleechantest`
- Bundle layout: `evidence/repro-8160/REPRO.md` + `evidence/repro-8160/capture_firestore_state.py` + `evidence/repro-8160/firestore-snapshots/{baseline-pre,post-fix}.json`

## Connections

- [[SpellSlotFallback]] — older related fallback UX (different problem: empty spells array, not rest-reset)
- [[ZFC-Level-Up-Architecture]] — level-up contract this spec inherits from
- [[feedback-2026-07-05-partial-spell-slot-fix-vs-canonical-spec]] — case study: PR #8162 attempted this without reading the spec first
