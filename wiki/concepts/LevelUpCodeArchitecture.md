---
title: "Level-Up Code Architecture"
type: concept
tags: [architecture, level-up, rewards-box, world_logic, game_state, separation-of-concerns, llm_parser, rewards_engine, single-responsibility]
sources: [pr-6262-6263-6264-6268-level-up-pr-chain]
last_updated: 2026-04-14
---

# Level-Up Code Architecture: v3 (CURRENT)

**Supersedes**: All 4 open PRs (#6262, #6263, #6264, #6268 — close all)
**Branch**: `feat/rewards-engine-single-responsibility` off origin/main

## Core Rule: No File Twice

Once `llm_parser.py` starts the loop, every file is called exactly once, in order. The chain is linear. No file revisits another file already called.

## v3 Flow

```
llm_parser.py  ─────────────────────────────────────────────────
  │  ONE entry point for both streaming AND non-streaming
  │
  ├─ game_state.py ──→ LevelProgressionState
  │                      {stored_level, resolved_target_level,
  │                       xp_gained, pending_rewards, xp_to_next_level}
  │                      Pure D&D 5e math + Firestore I/O.
  │                      NO rewards building, NO modal logic.
  │
  ├─ rewards_engine.py ──→ canonical (rewards_box, planning_block)
  │                      IDEMPOTENT — called by DeferredRewardsProtocol
  │                      every 10 turns. DNC type coercion.
  │                      ONE should_show_rewards_box() decision.
  │
  ├─ world_logic.py ──→ modal injection + planning assembly
  │                      THIN WRAPPER — receives pre-computed payload.
  │                      DOES NOT call back into game_state or
  │                      rewards_engine.
  │
  ├─ Persist to Firestore
  │
  └─ Return to frontend
         ├── Streaming: yield done event SSE
         └── Non-streaming: unified_response JSON
```

## File Responsibilities

| File | ONE Job | Does NOT Do |
|------|---------|------------|
| `llm_parser.py` | Parse LLM response, orchestrate full loop | XP math, rewards building, modal logic |
| `game_state.py` | Firestore I/O + D&D 5e XP/level math | Rewards building, modal logic |
| `rewards_engine.py` | ALL rewards computation: build, normalize, decide. IDEMPOTENT | Firestore I/O, modal logic |
| `world_logic.py` | Thin modal wrapper only | game_state calls, rewards_engine calls |
| `app.js` | Pure render | Logic, type coercion |

## Key Properties

### DeferredRewardsProtocol Integration
The background system (runs every 10 player turns) calls `rewards_engine` to fill gaps. **rewards_engine must be idempotent** — calling it twice with same inputs = same outputs. Must use `rewards_processed` flags to prevent double-counting.

### DNC Type Coercion
`normalize_rewards_box` uses DefensiveNumericConversion: `"true"/"1"/true → True`, `"false"/"0"/false → False`, numeric strings → int. Sentinel: `normalize_rewards_box({}) is None`.

### ASI Class-Specific Levels
- All classes: 4, 8, 12, 16, 19
- Fighter extra: **level 6**
- Rogue extra: **level 10**

### Multi-Level-Up
If one XP award crosses multiple thresholds (e.g., 5000 XP = level 1→7), iterate one level at a time. Each iteration produces one `rewards_box`. Frontend sequences the modals.

### Architectural Tests (mandatory)
```python
def test_world_logic_does_not_import_game_state():
    import world_logic
    assert 'game_state' not in dir(world_logic)

def test_world_logic_does_not_import_rewards_engine():
    import world_logic
    assert 'rewards_engine' not in dir(world_logic)
```

## Property-Based Tests (mandatory)
```python
@given(xp=st.integers(0, 500000))
def test_xp_never_overflows_level_20(xp):
    assert 1 <= level_from_xp(xp) <= 20

def test_normalize_coerces_all_formats():
    assert normalize_rewards_box({"xp_gained": "500", "level_up_available": "true"})["xp_gained"] == 500
    assert normalize_rewards_box({}) is None  # sentinel

def test_asi_levels_fighter_includes_6():
    assert _is_asi_level(6, "Fighter") is True
    assert _is_asi_level(6, "Rogue") is False
```

---

## BEFORE: Broken Architecture (all 4 PRs had same bugs)

The level-up / rewards_box pipeline had **scattered responsibility** across 4 files:

## BEFORE: Current Architecture (origin/main)

### Responsibility Map

```
LLM Response
    ↓
streaming_orchestrator.py: stream_story_with_game_state (done event)
    ↓ (conditionally)
world_logic._resolve_canonical_level_up_ui_pair()  [line 1742]
    ├── IF _has_level_up_ui_signal=False
    │   ├── normalize_planning_block_choices()  [passthrough]
    │   └── normalize_rewards_box_for_ui() → rewards/builder.py:normalize_rewards_box_for_ui()
    │       (NOT called in passthrough — BUG #6265)
    │
    └── IF _has_level_up_ui_signal=True
        ├── _project_level_up_ui_from_game_state()  [line 1686]
        │   ├── game_state.resolve_level_progression_state()  [game_state.py:979]
        │   ├── game_state.ensure_level_up_rewards_pending()  [game_state.py:1294]
        │   ├── world_logic._enforce_rewards_box_planning_atomicity()  [world_logic.py:2842]
        │   └── world_logic.build_level_up_rewards_box()  [world_logic.py:251]
        └── [level_up modal active path]
            └── ...
```

### File Responsibilities (CURRENT — origin/main)

| File | Functions | Responsibility |
|------|-----------|----------------|
| `game_state.py` | `extract_character_xp` [937] | XP value extraction from player data |
| `game_state.py` | `resolve_level_progression_state` [979] | Canonical level/XP state from game state |
| `game_state.py` | `resolve_level_up_signal` [1214] | Detect active level-up signal |
| `game_state.py` | `ensure_level_up_rewards_pending` [1294] | Set/clear `rewards_pending` flags |
| `game_state.py` | `normalize_pending_rewards` [1163] | Normalize rewards_pending dict |
| `game_state.py` | `validate_and_correct_state` [3741] | State validation + canonicalization |
| `game_state.py` | `_is_state_flag_true/false` | Boolean coercion from LLM strings |
| `world_logic.py` | `normalize_rewards_box_for_ui` [122] | Normalize LLM rewards_box keys (NOT exported to rewards/) |
| `world_logic.py` | `_has_level_up_ui_signal` [1725] | Check if level-up is active |
| `world_logic.py` | `_resolve_canonical_level_up_ui_pair` [1742] | Central resolver — single source of truth |
| `world_logic.py` | `_project_level_up_ui_from_game_state` [1686] | Project canonical rewards_box + planning |
| `world_logic.py` | `_enforce_rewards_box_planning_atomicity` [2842] | Enforce rewards/planning consistency |
| `world_logic.py` | `build_level_up_rewards_box` [251] | Build rewards_box from pending rewards |
| `world_logic.py` | `_extract_level_up_loot` [232] | Extract loot from rewards_pending |
| `world_logic.py` | `_inject_levelup_choices_if_needed` | Inject ASI/feat level-up choices |
| `world_logic.py` | `inject_persisted_living_world_fallback` [4271] | Living world fallback injection |
| `streaming_orchestrator.py` | `stream_story_with_game_state` [532] | Streaming done-event handler |
| `streaming_orchestrator.py` | `_resolve_canonical_level_up_ui_pair` call | Normalizes rewards_box on streaming |

### Key Problems with Current Architecture

1. **`normalize_rewards_box_for_ui` in TWO places** — once at world_logic.py:122 (from rewards.builder) and used but not defined in world_logic.py
2. **`_has_level_up_ui_signal` controls BOTH passthrough AND active path** — passthrough path was bypassing normalization (bug #6265, now fixed)
3. **`build_level_up_rewards_box` AND `_build_level_up_rewards_box_from_pending`** — two similar functions, possibly duplicated
4. **`game_state.py` owns BOTH XP extraction (`extract_character_xp`) AND level state (`resolve_level_progression_state`)** — good, but the calling patterns are complex
5. **`_enforce_rewards_box_planning_atomicity` is 60+ lines** — handles many edge cases but is a single monolithic function
6. **Stuck-completion synthesis is DUPLICATED** in `ensure_level_up_rewards_box` and `ensure_level_up_planning_block` and inline in `_project_level_up_ui_from_game_state`

---

## AFTER: Target Architecture

The goal is **pipeline clarity**:

```
LLM Raw Response
    ↓
[1] PARSE — extract structured fields
    world_logic: stream response parsing
    →
[2] NORMALIZE — call normalize_rewards_box_for_ui (ALL paths)
    normalize_rewards_box_for_ui (single location, always called)
    →
[3] CALCULATE — XP/level/rewards computation
    game_state: extract_character_xp(), resolve_level_progression_state()
    game_state: resolve_level_up_signal(), ensure_level_up_rewards_pending()
    →
[4] ENFORCE — atomicity + consistency
    world_logic: _enforce_rewards_box_planning_atomicity()
    world_logic: stuck-completion synthesis (SINGLE function, not 3 copies)
    →
[5] FORMAT — decide what to display
    world_logic: _resolve_canonical_level_up_ui_pair() — returns canonical pair
    →
[6] PERSIST — streaming passthrough
    streaming_orchestrator: calls normalize_rewards_box_for_ui unconditionally
    →
[7] UI — display decision
    frontend: app.js — decides whether to show rewards_box
```

### Proposed File Responsibilities (TARGET)

| File | Responsibility | Functions |
|------|----------------|-----------|
| `streaming_orchestrator.py` | **Entry point** — raw response → normalize | Always calls `normalize_rewards_box_for_ui` before Firestore write |
| `world_logic.py` | **Orchestration + atomicity** — resolve, enforce, project | `_resolve_canonical_level_up_ui_pair`, `_enforce_rewards_box_planning_atomicity`, stuck-completion synthesis |
| `game_state.py` | **Pure computation** — XP, level, state flags | `extract_character_xp`, `resolve_level_progression_state`, `resolve_level_up_signal`, flag helpers |
| `rewards/builder.py` | **Rewards assembly** — build rewards_box from pending | `build_level_up_rewards_box`, loot extraction, ASI injection |
| `app.js` | **Display gate** — decides whether to show UI | `debugMode` gate, `xp_gained > 0` gate |

### Key Rules

1. **`normalize_rewards_box_for_ui` is called ONCE, at the RIGHT place** — streaming_orchestrator, before Firestore write
2. **No passthrough bypass** — `_has_level_up_ui_signal` does NOT gate the normalize call
3. **Stuck-completion synthesis in ONE place** — `ensure_level_up_rewards_box` (called by `_resolve_canonical_level_up_ui_pair`)
4. **`ensure_level_up_planning_block` is INTEGRATED or REMOVED** — not dead code
5. **game_state.py is PURE** — no atomicity logic, no display formatting, only computation
6. **`_enforce_rewards_box_planning_atomicity` is SPLIT** if it exceeds ~40 lines

---

## What PRs #6262/6263/6264 Actually Change

| PR | Main Change | Architectural Impact |
|----|-------------|---------------------|
| #6264 | Moves `_is_state_flag_true/false` into world_logic.py; adds `ensure_level_up_rewards_box/planning_block`; stuck-completion synthesis (BUT HAS OFF-BY-ONE BUG); dead `ensure_level_up_planning_block` never called | Moves code between files, does NOT achieve single-responsibility |
| #6263 | Adds stuck-completion synthesis to `_project_level_up_ui_from_game_state` | Duplicates stuck-completion logic further |
| #6262 | Adds `_enforce_level_up_rewards_planning_atomicity` (DUPLICATE dead function); fixes stale flag detection | Adds redundant code |

### Problems with the PRs as Currently Written

1. **Off-by-one in stuck-completion**: `target_level = current_level + 1` when `level_up_complete=True` — wrong because level is already incremented
2. **Wrong dict keys**: `"target_level"` / `"level"` instead of `"resolved_target_level"` / `"stored_level"`
3. **Dead function**: `ensure_level_up_planning_block` is 110+ lines never called from production
4. **Duplicated synthesis logic**: 3 copies of stuck-completion synthesis across helpers
5. **Missing `freeze_time`**: synthesized choices missing `freeze_time: True`
6. **Production regression**: `inject_persisted_living_world_fallback` signature changed — breaks main.py caller

---

## What Would Actually Achieve Single Area Responsibility

### Streaming Orchestrator (Layer 6 — Entry/Persist)
```
streaming_orchestrator.py:
  stream_story_with_game_state(done_event)
    → ALWAYS call normalize_rewards_box_for_ui(raw_rewards_box)  ← ONE place
    → Write to Firestore
```
**Rule**: streaming_orchestrator NEVER does XP math or atomicity. It only normalizes and persists.

### world_logic (Layer 4 — Enforce + Format)
```
world_logic.py:
  _resolve_canonical_level_up_ui_pair()  ← ONE canonical resolver
    → _has_level_up_ui_signal()  [decision only, no mutation]
    → IF passthrough: return (normalized_rewards, planning)
    → IF active: _project_level_up_ui_from_game_state()
        → game_state.resolve_level_progression_state()  [pure compute]
        → rewards.build_level_up_rewards_box()  [assembly]
        → _enforce_atomicity()  [SPLIT if >40 lines]
        → _inject_choices_if_needed()  [ASI, feat]

  _enforce_rewards_box_planning_atomicity()  [REFACTOR: extract sub-functions]
    → _suppress_if_stale()  [new]
    → _inject_minimal_if_missing()  [new]
```
**Rule**: world_logic orchestrates but does NOT do raw XP extraction (that's game_state).

### game_state (Layer 3 — Pure Computation)
```
game_state.py:
  extract_character_xp(player_data) → int
  resolve_level_progression_state(state_dict) → {stored_level, resolved_target_level, pending_rewards}
  resolve_level_up_signal(state_dict) → bool
  ensure_level_up_rewards_pending(state_dict) → state_dict  [mutates, returns]
  _is_state_flag_true/false(val) → bool
```
**Rule**: game_state has ZERO display formatting, ZERO Firestore I/O, ZERO LLM response parsing.

### rewards/builder (Layer 3/4 — Assembly)
```
rewards/builder.py:
  normalize_rewards_box_for_ui(raw_box) → normalized_box | None
  build_level_up_rewards_box(state_dict, target_level, pending) → rewards_box
  _extract_level_up_loot(pending) → list[str]
  _inject_asi_choices_if_needed(rewards_box, target_level, player_class) → rewards_box
```
**Rule**: rewards/builder is the ONLY module that knows rewards_box structure.

---

## Polling Path Architecture

The v4 design has **three distinct paths** that converge on the same rewards engine entry points:

```
Path A (SSE Streaming):  llm_parser.py → rewards_engine.canonicalize_rewards()
Path B (HTTP GET):      llm_parser.py → rewards_engine.project_level_up_ui()
Path C (MCP Polling):   llm_parser.py → rewards_engine.project_level_up_ui()
```

### Path A: Streaming (Primary — SSE Push)
Frontend POSTs to `/interaction/stream` → receives story chunks via SSE → `done` event contains `rewards_box` inline. **No polling**. See [[LevelUpPolling]] for details.

### Path B: HTTP GET — Page Load Only
GET `/api/campaigns/<id>` → `get_campaign_state_unified` → returns full campaign state. **Initial page load only**. After page load, SSE takes over. Source: `world_logic.py:get_campaign_state_unified` lines 7454-7596.

### Path C: MCP Polling — External Clients
External clients (mobile, integrations) call `get_campaign_state` MCP tool → builds rewards_box from `game_state.rewards_pending`. **True polling**. Idempotency of `rewards_engine.canonicalize_rewards()` is critical.

### Polling Call Chain
```
get_campaign_state_unified()
  └→ _project_level_up_ui_from_game_state()
       └→ game_state.resolve_level_progression_state()
       └→ game_state.resolve_level_up_signal()
       └→ game_state.ensure_level_up_rewards_pending()
       └→ rewards_engine.build_level_up_rewards_box()
       └→ _enforce_rewards_box_planning_atomicity()
```

Both `canonicalize_rewards()` and `project_level_up_ui()` converge on `_canonicalize_core()`.

### DeferredRewardsProtocol — LLM Instruction, Not Timer
`DeferredRewardsProtocol` is NOT a server-side timer or cron job. It is an **LLM prompt instruction**: "Every 10 player turns, check whether any rewards have been missed." The LLM counts turns and triggers the check. `rewards_engine` must be IDEMPOTENT so repeated calls don't double-count.

---

## Summary

| Aspect | Before (origin/main) | After PRs (broken) | Target |
|--------|---------------------|---------------------|--------|
| normalize call site | streaming_orchestrator (FIXED #6265) | same | streaming_orchestrator only |
| stuck-completion | inline or missing | 3 copies + off-by-one bugs | 1 function |
| flag helpers location | game_state.py | world_logic.py (duplicated) | game_state OR world_logic, not both |
| atomicity function | `_enforce_rewards_box_planning_atomicity` (monolithic) | same + duplicate dead function | split into sub-functions |
| ASI injection | inline in `_inject_levelup_choices_if_needed` | scattered | `rewards.inject_asi_if_needed()` |
| dead code | minimal | significant (`ensure_level_up_planning_block`) | zero |

**The PRs #6262/6263/6264 do NOT achieve the target architecture** — they add complexity, duplicate logic, and introduce new bugs. A cleaner approach would be: fix the off-by-one in stuck-completion, remove dead `ensure_level_up_planning_block`, split `_enforce_rewards_box_planning_atomicity` into sub-functions, and keep flag helpers in `game_state.py`.
