---
title: "Level-Up Engine Single-Responsibility Design (2026-04-14)"
type: source
tags: [level-up, rewards-engine, architecture, worldarchitect, TDD, design]
date: 2026-04-14
source_file: raw/level-up-engine-single-responsibility-design-2026-04-14.md
---

## Summary

A design for refactoring the level-up/rewards logic in worldarchitect.ai from scattered responsibilities across 4 files (world_logic.py, game_state.py, streaming_orchestrator.py, agents.py) into a single-responsibility pipeline with `llm_parser.py` as one orchestration root calling into `rewards_engine.py` as the rewards decision engine. Design prescribes 4-layer TDD: RED (contract tests) → GREEN (pure impl) → WIRE (integration) → CLEAN (delete dupes).

## Key Claims

- `llm_parser.py` is the SINGLE orchestration root for streaming, non-streaming, and polling paths — no file called twice
- `world_logic.py` handles flag-driven UI state synthesis: modal injection, STUCK COMPLETION detection (level_up_complete=True but rewards_box absent), and stateful orchestration. It calls rewards_engine functions where appropriate.
- `rewards_engine.py` owns causal XP-threshold computation: given XP in, determine if level-up should fire, build rewards_box, atomicity, normalization, visibility decision
- `game_state.py` owns D&D 5e XP math + Firestore I/O only — no flag interpretation
- 4-layer TDD with mandatory gates: RED (8 failing tests) → GREEN (all pass) → WIRE → CLEAN
- Layer 3 CLEAN: delete constants.py XP dupes, reduce agents.py 110→3 lines, remove app.js boolean coercion

## Key Quotes

> "world_logic.py handles flag-driven UI state synthesis: modal injection, STUCK COMPLETION detection, stateful orchestration. It calls rewards_engine where appropriate for causal computation."

> "rewards_engine.py handles XP-threshold computation given state — it does NOT synthesize missing rewards_box from flags (STUCK COMPLETION is world_logic responsibility)."

> "Behavioral equivalence audit (2026-04-15): 0/5 function pairs between world_logic.py and rewards_engine.py are equivalent. Key difference: STUCK COMPLETION synthesis (level_up_complete=True but box absent) is world_logic-only."

> "Single forward pass — no file called twice, no re-canonicalization or re-fetch of XP in the same request."

## Two-Path Architecture

The level-up/rewards system has two separate, non-overlapping paths:

**Path 1 — rewards_engine (causal/XP-threshold, polling)**
- Entry: `canonicalize_rewards()` (streaming/non-streaming) or `project_level_up_ui()` (polling)
- Responsibility: given XP in game_state, determine if level-up should fire, build canonical rewards_box, atomicity, normalization, visibility decision
- **Does NOT** handle: loot, gold, XP math, STUCK COMPLETION synthesis, modal injection
- **Does NOT** reference: loot, gold, coin, treasure anywhere in the module

**Path 2 — world_logic (flag-driven/stateful, streaming)**
- Entry: `_project_level_up_ui_from_game_state()`, `_maybe_trigger_level_up_modal()`
- Responsibility: flag-driven UI state synthesis, STUCK COMPLETION detection (level_up_complete=True but rewards_box absent), modal injection, loot/gold extraction from LLM output
- Handles: XP synthesis, combat rewards, encounter rewards, narrative rewards
- **Does NOT** call rewards_engine public API (is_level_up_active, project_level_up_ui, resolve_level_up_signal)

**Key**: The design doc's original claim that "5 world_logic functions map to rewards_engine equivalents" was incorrect. There is no 1:1 mapping — two separate architectural paths.

## Loot/Gold Extraction Audit (rev-v4ci07)

Loot and gold extraction exists **entirely in world_logic.py** — rewards_engine.py has zero references to loot, gold, coin, or treasure.

### Locations in world_logic.py

| Function | What it extracts |
|---|---|
| `_normalize_rewards_box_fields()` | gold from aliases (gold, gold_awarded, goldAmount, gp, gold_earned, gold_pieces); loot from list |
| `_extract_level_up_loot()` | loot from `rewards_pending["items"]` |
| `build_level_up_rewards_box()` | gold + loot from rewards_pending state |
| `_synthesize_generic_rewards_box()` | gold + loot from combat/loot state |
| `build_generic_rewards_box()` | gold + loot from game_state |
| `build_encounter_rewards_box()` | gold + loot from encounter_state |
| `build_narrative_rewards_box()` | hardcoded: gold=0, loot=[] |

### Design Doc vs. Actual Divergence

The design doc stated "rewards_engine.py owns ALL rewards/progression decisions" — loot/gold was implicitly included in scope. In practice, loot/gold extraction:
- Never moved to rewards_engine
- Stayed entirely in world_logic
- Is tightly coupled to LLM output parsing (multiple alias normalization, item name extraction)

### Recommendation: Keep in world_logic

Loot/gold extraction should **stay in world_logic.py** for the following reasons:

1. **LLM coupling**: loot/gold extraction requires parsing multiple field name aliases from LLM output (gold_awarded, goldAmount, gp, items, loot, etc.) — this is a streaming/parsing concern, not a causal computation concern
2. **No rewards_engine need**: rewards_engine works on canonical game_state XP; it has no need for loot/gold which is purely cosmetic/reward display
3. **Scope creep risk**: moving loot/gold to rewards_engine would require rewards_engine to understand LLM output field names, which breaks the causal/XP-threshold contract
4. **No atomicity requirement**: loot/gold and level-up are in the same rewards_box but have independent semantics — no causal dependency requiring shared normalization

**Decision**: loot/gold extraction remains world_logic responsibility. rewards_engine scope is XP-threshold + level-up decisions only.

## Drift: What Was NOT Implemented in PR #6276

- **constants.py** still has duplicate `get_xp_for_level` / `get_level_from_xp` — design says DELETE
- **agents.py** `_is_stale_level_up_pending` not reduced to 3-line delegate — design says 110→3
- **Browser UI video evidence** not produced — design requires captioned browser UI for `/es` gate

## Connections
- [[LevelUpCodeArchitecture]] — architecture concept page documenting the v3/v4 pipeline
- [[RewardsEngine]] — rewards_engine concept page
- [[LevelUpPolling]] — polling vs streaming paths
- [[PRWatchdog]] — PR monitoring workflow
- [[Harness5LayerModel]] — harness framework for preventing drift

## Implementation Status

| Layer | Status | PR |
|-------|--------|-----|
| Layer 0 RED | Done (8 failing → passing tests) | PR #6273 |
| Layer 1 GREEN | Done | PR #6273 |
| Layer 2 WIRE | Done (wired to rewards_engine) | PR #6273 |
| Layer 3 CLEAN | INCOMPLETE — constants.py dupes remain, agents.py unreduced | PR #6276 |
| Architecture Corrective | Done — design doc corrected: two-path architecture, world_logic is NOT pure consumer | rev-v4ci06 |
| Loot/Gold Audit | Done — documented loot/gold stays in world_logic; rewards_engine has no loot/gold references | rev-v4ci07 |

## Root Cause of Drift

Design was not used as a checkable contract during implementation. No automated gate verifying world_logic.py has zero rewards_engine calls. Parallel agents diverged from design without reconciliation.

**Corrective update (2026-04-15)**: Behavioral equivalence audit revealed the "world_logic as pure consumer" design goal is architecturally incorrect. Two-path model: rewards_engine (causal/XP-threshold), world_logic (flag-driven/stateful including STUCK COMPLETION, loot/gold). Loot/gold extraction stays in world_logic — rewards_engine has zero references to it.

**rev-v4ci07 update (2026-04-15)**: loot/gold extraction audit confirms all extraction lives in world_logic.py (7 functions). rewards_engine.py has zero loot/gold references. Recommendation: keep in world_logic — LLM output parsing coupling makes moving inappropriate.
