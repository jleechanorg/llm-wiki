---
title: "Rewards Engine: Single-Responsibility Pipeline Refactor"
type: source
tags: [level-up, rewards, architecture, worldarchitect]
date: 2026-04-14
source_file: ../roadmap/level-up-engine-v4-design.md
---

## Summary

The Level-Up Engine v4 design is a comprehensive single-responsibility pipeline refactor that unifies the scattered rewards/level-up logic across streaming, non-streaming, and polling paths. The design consolidates 4 files with duplicated detection into 3 clean layers: `llm_parser.py` (orchestration root), `rewards_engine.py` (decisions), and `game_state.py` (XP math). This closes PRs #6262, #6263, #6264, #6268 with a clean implementation.

## Problem

Level-up/rewards logic is scattered across 4 files with duplicated detection, 3 copies of `_is_state_flag_true`, and 25+ functions in `world_logic.py`. Four open PRs attempted partial fixes but duplicate each other (#6263 and #6264 add identical functions). The streaming and non-streaming paths apply different postconditions at persistence time, causing `rewards_box`/level-up flag divergence.

## Core Tenet

**Streaming and non-streaming MUST NOT have different files in the flow.** They share the same pipeline, same functions, same file sequence. The only difference is the transport at the end (SSE vs JSON).

## Architecture: Single-Responsibility Pipeline

**Rule: single forward pass — no file called twice, no re-canonicalization or re-fetch of XP in the same request.**

| Stage | File | Responsibility |
|-------|------|----------------|
| Stage 1: FETCH+PARSE | `llm_parser.py` | Parse LLM response → structured fields |
| Stage 2: XP MATH | `game_state.py` | Level, XP numbers |
| Stage 3: DETECT+BUILD | `rewards_engine.py` | `rewards_box`, `planning_block` |
| Stage 4: NORMALIZE | `rewards_engine.py` | Clean types, `should_show` |
| Stage 5: MODAL+STORY | `world_logic.py` | Modal injection, story assembly |
| Stage 6: PERSIST | `llm_parser.py` | Firestore write |
| Stage 7: RENDER | `app.js` | Pure render, zero logic |

## ONE Orchestration Root: `llm_parser.py`

`llm_parser.py` (renamed from `streaming_orchestrator.py`) is the SINGLE entry point for all LLM response processing. It already handles both streaming token assembly and non-streaming JSON parsing. Three entry points converge on ONE pipeline:

- `stream_and_process()` — streaming POST
- `process_action()` — non-streaming POST (moved from `world_logic`)
- `get_campaign_state()` — polling GET (moved from `world_logic`)

### Call-Graph Rule

Each request calls rewards_engine **once** via exactly one of:
- `canonicalize_rewards()` — streaming or non-streaming (both use this)
- `project_level_up_ui()` — polling only (no LLM output to parse)

After that call, `world_logic.inject_modal_state()` wraps the result. No file re-enters the pipeline.

## New File: `mvp_site/rewards_engine.py`

### Public API (~7 functions)

```python
# --- Signal Detection ---
def is_level_up_active(game_state_dict: dict) -> bool:
    """ONE detector. Replaces 3 parallel checks in agents.py, game_state.py, world_logic.py.
    Also checks character_creation active — returns True if CC or level-up in progress."""

def resolve_level_up_signal(game_state_dict: dict, rewards_box: dict | None = None) -> tuple[bool, int | None, bool]:
    """ONE resolver. Moved from game_state.py. Calls game_state.level_from_xp() internally."""

# --- Rewards Building (atomic pair) ---
def ensure_rewards_box(game_state_dict: dict) -> dict | None:
    """Build canonical level-up rewards_box from game state. Atomic with ensure_planning_block."""

def ensure_planning_block(game_state_dict: dict) -> dict | None:
    """Build canonical planning_block. Atomic with ensure_rewards_box."""

# --- UI Formatting ---
def normalize_rewards_box(rewards_box: dict | None) -> dict | None:
    """ONE normalizer. Guarantees clean booleans, coerced ints. Returns None if empty."""

def should_show_rewards_box(rewards_box: dict | None) -> bool:
    """ONE visibility decision. Replaces scattered checks in world_logic + app.js."""

# --- Two Entry Points (both converge to _canonicalize_core) ---
def canonicalize_rewards(structured_fields: dict, game_state_dict: dict,
                         original_state_dict: dict | None = None) -> tuple[dict | None, dict | None]:
    """STREAMING + NON-STREAMING path. Called by llm_parser.py."""

def project_level_up_ui(game_state_dict: dict) -> tuple[dict | None, dict | None]:
    """POLLING path. No LLM output — re-derives from game_state flags."""

# --- Internal ---
def _canonicalize_core(raw_rewards_box, raw_planning_block, game_state_dict,
                       original_state_dict=None) -> tuple[dict | None, dict | None]:
    """ALL paths converge here. 100% shared logic."""
```

### Dependency Direction

```
game_state.py → rewards_engine.py → llm_parser.py
                                  → world_logic.py
                                  → agents.py
```

`game_state.py` does NOT import `rewards_engine.py`. Strict one-way dependency.

### Idempotency Requirement

`rewards_engine` **must be idempotent**: calling `canonicalize_rewards()` twice with the same inputs MUST produce the same outputs. This is critical for the [[DeferredRewardsProtocol]] which calls rewards_engine every 10 player turns. The idempotency invariant: `canonicalize(x, y, z) == canonicalize(x, y, z)` regardless of how many times called.

## Known Bugs Fixed in Clean Rewrite

| Bug | PRs affected | Fix |
|-----|-------------|-----|
| Off-by-one: `target_level = current_level + 1` when `level_up_complete=True` | #6262, #6263, #6264 | `resolve_level_up_signal` checks `level_up_complete` flag before incrementing |
| Wrong dict keys: `"target_level"` / `"level"` instead of `"resolved_target_level"` / `"stored_level"` | #6262 | Consistent key names throughout engine |
| Dead function: `ensure_level_up_planning_block` (~110 lines, never called) | #6264 | `ensure_planning_block()` is always called atomically with `ensure_rewards_box()` |
| Missing `freeze_time: True` on synthesized stuck-completion choices | #6263, #6264 | Set in `ensure_planning_block()` when synthesizing |
| ASI injection checks `current_level` instead of `new_level` (target level) | #6263 | `_is_asi_level(target_level)` not `_is_asi_level(current_level)` |
| `inject_persisted_living_world_fallback` TypeError from signature change | #6264 | world_logic.py signature stabilized |

## PR Strategy

1. Close PRs #6262, #6263, #6264, #6268 with comment linking to this design
2. Cherry-pick test files from #6263/#6264
3. One clean PR against main (`feat/rewards-engine-single-responsibility`)
4. Estimated net: +800 lines (new engine) / -1200 lines (removed from world_logic/game_state/agents) = **-400 net lines**

## Implementation Order

1. `git mv streaming_orchestrator.py llm_parser.py` + update imports
2. Create `rewards_engine.py` with full public API
3. Wire `llm_parser.py` to call rewards_engine
4. Move non-streaming orchestration from `world_logic.py` into `llm_parser.py`
5. Strip `world_logic.py` to thin modal wrapper
6. Update `agents.py` to delegate to rewards_engine
7. Delete duplicate XP math from `constants.py`
8. Clean `app.js` boolean coercion (server now guarantees types)

## What Moves Where

| Current Location | Function | Destination |
|---|---|---|
| `world_logic.py` | `_resolve_canonical_level_up_ui_pair()` | `rewards_engine._canonicalize_core()` |
| `world_logic.py` | `_project_level_up_ui_from_game_state()` | `rewards_engine.project_level_up_ui()` |
| `world_logic.py` | `_enforce_rewards_box_planning_atomicity()` | `rewards_engine._enforce_atomicity()` |
| `world_logic.py` | `_should_emit_level_up_rewards_box()` | `rewards_engine.should_show_rewards_box()` |
| `world_logic.py` | `_has_level_up_ui_signal()` | `rewards_engine.resolve_level_up_signal()` |
| `world_logic.py` | `normalize_rewards_box_for_ui()` | `rewards_engine.normalize_rewards_box()` |
| `world_logic.py` | `process_action_unified()` orchestration | `llm_parser.py` |
| `world_logic.py` | `get_campaign_state_unified()` orchestration | `llm_parser.py` |
| `game_state.py` | `resolve_level_up_signal()` | `rewards_engine` (thin redirect stays) |
| `game_state.py` | `ensure_level_up_rewards_pending()` | `rewards_engine` (thin redirect stays) |
| `game_state.py` | `_is_state_flag_true()` | `rewards_engine` (ONE version) |
| `agents.py` | `_is_character_creation_or_level_up_active()` (110 lines) | 3-line delegate to `rewards_engine.is_level_up_active()` |

## Connections

- [[SingleResponsibilityPipeline]] — 7-stage pipeline concept
- [[RewardsEngineIdempotency]] — idempotency requirement for rewards_engine
- [[DeferredRewardsProtocol]] — runs every 10 turns, calls rewards_engine
- [[DefensiveNumericConversion]] — type normalization in normalize_rewards_box
- [[LevelUpModalRouting]] — modal state signals and constraints
- [[RewardsBoxAtomicity]] — rewards_box + planning_block atomicity invariants
- [[LevelUpBugInvestigation]] — prior bug investigation
- [[LevelUpCodeArchitecture]] — v3 architecture precedent
- [[StreamingOrchestrator]] — original streaming orchestrator (now renamed to llm_parser)
