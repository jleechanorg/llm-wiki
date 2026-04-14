---
title: "Layer3CleanRefactor"
type: concept
tags: [worldarchitect-ai, architecture, rewards-engine]
sources: [test-prs/pr-6276-layer3-clean-strip-rewards-detection.md]
last_updated: 2026-04-14
---

## What It Is

Layer 3 of a multi-layer rewards engine single-responsibility refactor. Strips `world_logic.py` of deprecated rewards detection functions, wiring it strictly to `rewards_engine` public API.

## Problem It Solves

`world_logic.py` had accumulated duplicate rewards detection logic (`build_level_up_rewards_box`, `_project_level_up_ui_from_game_state`, 7 call sites of `resolve_level_up_signal`) that duplicated what `rewards_engine` already provided via `project_level_up_ui()` and `is_level_up_active()`. This violated single-responsibility: world_logic was both a consumer AND a producer of rewards data.

## How It Works

**Deleted (91 lines):**
- `build_level_up_rewards_box()` (54 lines) — replaced by `project_level_up_ui()`
- `_project_level_up_ui_from_game_state()` (37 lines) — replaced by `project_level_up_ui()`
- 7 call sites of `resolve_level_up_signal` — replaced by `is_level_up_active()`

**Added:**
- `llm_service = _lazy_module("mvp_site.llm_service")` — defers google.genai loading, saves ~840ms cold-start
- MOCK_SERVICES_MODE guard around Firebase initialization

**New imports kept:**
- `is_level_up_active`, `project_level_up_ui`, `should_show_rewards_box`

## Why It Matters

Single-responsibility violations cause cascading regressions (see C6 pattern). When one module both produces and consumes data, atomicity guarantees break. `world_logic` should consume canonical state, not reconstruct it.

## Architecture Layers

| Layer | State | Description |
|---|---|---|
| Layer 0 | RED | 15 failing contract tests for rewards_engine.py |
| Layer 1 | GREEN | Single-responsibility rewards engine (rewards_engine.py owns normalization) |
| Layer 2 | RED | Integration wiring tests (failing, to be green after WIRE layer) |
| Layer 3 | CLEAN | world_logic.py strips old detection, uses rewards_engine public API |

## Results on My Codebase (Cycle 19 — 2026-04-14)

**Canonical Score: 77/100**

| Dimension | Verdict |
|---|---|
| Naming & Consistency | PASS |
| Error Handling | MARGINAL (MOCK_SERVICES_MODE guard, no runtime lazy-load error handling) |
| Type Safety (30%) | FAIL (213 `Any` in world_logic.py; TypedDict not introduced) |
| Test Coverage | FAIL (22 tests in test_level_up_stale_flags.py fail calling deleted functions) |
| Documentation | PASS (excellent deferred-loading comments) |
| Evidence Standard | MARGINAL (7/7 wiring tests pass; E2E cannot run locally) |

**Improvements identified:** Update test_level_up_stale_flags.py to use `project_level_up_ui()` instead of deleted functions; add TypedDict for structured data parameters; add try/except around lazy module usage.
