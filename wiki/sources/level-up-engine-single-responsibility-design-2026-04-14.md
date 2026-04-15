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
- `world_logic.py` becomes a "pure consumer" — receives pre-computed payload, injects modal state, calls ZERO rewards_engine functions
- `rewards_engine.py` owns ALL rewards/progression decisions: detection, building, atomicity, normalization, visibility
- `game_state.py` owns D&D 5e XP math + Firestore I/O only — no flag interpretation
- 4-layer TDD with mandatory gates: RED (8 failing tests) → GREEN (all pass) → WIRE → CLEAN
- Layer 3 CLEAN: delete constants.py XP dupes, reduce agents.py 110→3 lines, remove app.js boolean coercion

## Key Quotes

> "world_logic.py becomes a pure consumer — it receives pre-computed rewards data and wraps it with modal semantics. It does NOT call game_state for XP or rewards_engine for detection."

> "Single forward pass — no file called twice, no re-canonicalization or re-fetch of XP in the same request."

> "The aspirational v4 design (world_logic as 'thin modal wrapper only') was not fully achieved — orchestration wrappers remain at lines 1246, 1669, 1695, 1715." — PR #6276 body

## Drift: What Was NOT Implemented in PR #6276

- **world_logic.py still has 9× `project_level_up_ui()` + 1× `is_level_up_active()`** — design says ZERO
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
| Layer 3 CLEAN | INCOMPLETE — world_logic.py not stripped, constants.py dupes remain, agents.py unreduced | PR #6276 |

## Root Cause of Drift

Design was not used as a checkable contract during implementation. No automated gate verifying world_logic.py has zero rewards_engine calls. Parallel agents diverged from design without reconciliation.
