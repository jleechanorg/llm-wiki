# Rewards Engine: Single-Responsibility Pipeline Refactor

**Date**: 2026-04-14
**Status**: Design approved (v4 — single root, llm_parser.py unifies streaming/non-streaming)
**Supersedes**: PRs #6262, #6263, #6264, #6268 (all to be closed)
**Implementation branch**: `feat/rewards-engine-single-responsibility` (off main)
**Prior versions**: v3 had two orchestration roots; v4 merges into ONE per user directive

## Problem

Level-up/rewards logic is scattered across 4 files with duplicated detection, 3 copies of `_is_state_flag_true`, and 25+ functions in world_logic.py alone. Four open PRs attempted partial fixes but duplicate each other (#6263 and #6264 add identical functions). The merge sequence is fragile (#6268 patches code #6264 deletes).

Additionally, the streaming path (`streaming_orchestrator.py`) and non-streaming path (`world_logic.process_action_unified`) apply different postconditions at persistence time, causing rewards_box/level-up flag divergence.

## Core Tenet

**Streaming and non-streaming MUST NOT have different files in the flow.** They share the same pipeline, same functions, same file sequence. The only difference is the transport at the end (SSE vs JSON).

## Architecture: Single-Responsibility Pipeline

**Rule: single forward pass — no file called twice, no re-canonicalization or re-fetch of XP in the same request.**

```
Stage 1: FETCH+PARSE    llm_parser.py                         → structured fields
Stage 2: XP MATH        game_state.py                         → level, XP numbers
Stage 3: DETECT+BUILD   rewards_engine.py                     → rewards_box, planning_block
Stage 4: NORMALIZE      rewards_engine.py                     → clean types, should_show
Stage 5: MODAL+STORY    world_logic.py                        → modal injection, story assembly
Stage 6: PERSIST        llm_parser.py                         → Firestore write
Stage 7: RENDER         app.js                                → pure render, zero logic
```

## ONE Orchestration Root: `llm_parser.py`

`llm_parser.py` (renamed from `streaming_orchestrator.py`) is the SINGLE entry point for all LLM response processing. It already handles both streaming token assembly and non-streaming JSON parsing. The rename reflects this dual role.

### The Flow (identical for streaming and non-streaming)

```
llm_parser.py                                               ← SINGLE ROOT
│
├─ Receives LLM response (streaming tokens OR non-streaming JSON)
├─ Parses into structured_fields (rewards_box, planning_block, state_updates, etc.)
│
├─ game_state.py: extract XP math                           ← Stage 2
│   └─ level_from_xp(), extract_character_xp()
│   └─ Returns LevelProgressionState
│
├─ rewards_engine.canonicalize_rewards(                      ← SINGLE CALL (Stages 3-4)
│      structured_fields, game_state_dict,
│      original_state_dict)
│   │
│   └─ internally: resolve_level_up_signal()
│   └─ internally: ensure_rewards_box() + ensure_planning_block()
│   └─ internally: normalize_rewards_box()
│   └─ internally: should_show_rewards_box()
│   └─ Returns (rewards_box, planning_block) or (None, None)
│
├─ world_logic.inject_modal_state(                           ← Stage 5
│      rewards_box, planning_block, game_state_dict)
│   └─ Adds modal_triggered, modal_finish_choice, modal_lock
│   └─ Does NOT call game_state or rewards_engine again
│
├─ Persist to Firestore                                      ← Stage 6
│   └─ 6a. game_state update (XP, level, rewards_pending, flags)
│   └─ 6b. add_story_entry("user", user_action)
│   └─ 6c. add_story_entry("gemini", llm_response, structured_fields)
│   └─ 6d. enrichment (session header, living world fallback)
│   └─ Order matters: game_state before story entries (story reads latest state)
│
└─ Return to frontend                                        ← Stage 7
     ├── Streaming: yield SSE done event → app.js
     └── Non-streaming: return unified_response dict → app.js
```

### Polling Path (no LLM response)

```
llm_parser.py                                               ← SAME ROOT
│
├─ No LLM response — reads latest story entry from Firestore
├─ Extracts rewards_box, planning_block from stored entry
│
├─ If no stored rewards_box/planning_block:
│   rewards_engine.project_level_up_ui(game_state_dict)      ← SINGLE CALL
│   └─ Re-derives from game_state flags (no original_state_dict)
│   └─ Returns (rewards_box, planning_block) or (None, None)
│
├─ world_logic.inject_modal_state(...)                       ← Stage 5
│
└─ Return JSON response → app.js
```

#### Who Calls the Polling Path and When

The frontend does NOT poll via `get_campaign_state`. It uses `POST /api/campaigns/<id>/interaction/stream` (SSE), which returns rewards_box/planning_block inline in the SSE done event. The polling path fires in 3 scenarios only:

| Caller | When |
|---|---|
| **Game page load** | `GET /api/campaigns/<id>` — initial load only, then SSE takes over |
| **MCP clients** | External tools (mobile app, integrations) call `get_campaign_state` MCP tool |
| **Stale story entry** | Story entry lacks rewards_box/planning_block — rare recovery path |

This means `project_level_up_ui()` is NOT hot-polled in a tight loop. Rapid-fire idempotency concerns do not apply. The function must be pure/read-only for correctness, not for performance.

**Note**: `DeferredRewardsProtocol` is an LLM prompt instruction ("every N turns, check for missed rewards"), not a server-side polling timer. The LLM triggers the check via a normal streaming response, not via `get_campaign_state_unified`.

### Call-Graph Rule

Each request calls rewards_engine **once** via exactly one of:
- `canonicalize_rewards()` — streaming or non-streaming (both use this)
- `project_level_up_ui()` — polling only (no LLM output to parse)

After that call, `world_logic.inject_modal_state()` wraps the result. No file re-enters the pipeline.

## New File: `mvp_site/rewards_engine.py`

### Why `rewards_engine.py` (not `level_up_engine.py`)

The file handles more than level-up:
- **XP gains** (combat, encounters, narrative, god mode)
- **Loot** (items, gold from rewards_pending, combat_state)
- **Level-up detection** (threshold crossing, signal resolution)
- **Rewards box building** (combines XP + loot + level-up into UI payload)
- **Planning block for level-up choices** (ASI, ability scores)
- **Show/hide decision** (should_show_rewards_box)

### Dependency: imports from game_state.py (upstream)

```python
from mvp_site.game_state import (
    level_from_xp,          # D&D 5e XP → level lookup
    xp_needed_for_level,    # level → cumulative XP threshold
    xp_to_next_level,       # how much XP until next level
    extract_character_xp,   # robust XP extraction from player_data
    LevelProgressionState,  # dataclass
    coerce_int,             # robust int coercion
)
```

The engine NEVER duplicates XP math. It calls game_state for numbers, then makes decisions.

**game_state.py does NOT import rewards_engine.py.** Strict one-way dependency.

### `_is_state_flag_true` / `_is_state_flag_false`

These move INTO `rewards_engine.py` as the ONE canonical version. The 3 divergent copies (game_state, world_logic, agents inline) are all deleted. game_state.py imports from rewards_engine if it needs flag interpretation for its own Firestore reads.

**Exception**: If this creates a circular import (rewards_engine imports game_state, game_state imports rewards_engine), keep `_is_state_flag_true` in game_state.py and import from there. Prefer no circular dependency.

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
    """STREAMING + NON-STREAMING path. Called by llm_parser.py.
    Extracts raw rewards_box/planning_block from structured_fields, then _canonicalize_core()."""

def project_level_up_ui(game_state_dict: dict) -> tuple[dict | None, dict | None]:
    """POLLING path. No LLM output — re-derives from game_state flags.
    Passes raw=None to _canonicalize_core(), which builds from state."""
```

### `original_state_dict` Parameter

The `original_state_dict` parameter is a **snapshot of game_state before the LLM call**. It is used for:
- **Stale signal detection**: comparing pre-LLM XP to post-LLM XP to detect whether XP actually changed
- **Level-up threshold crossing**: `extract_character_xp(original) < xp_needed_for_level(target)` and `extract_character_xp(current) >= xp_needed_for_level(target)`

Required for streaming and non-streaming paths (both have a pre-LLM snapshot). Not available for polling (reads from persisted state only — no before/after).

### Internal: _canonicalize_core (THE shared computation)

```python
def _canonicalize_core(
    raw_rewards_box: dict | None,
    raw_planning_block: dict | None,
    game_state_dict: dict,
    original_state_dict: dict | None = None,
) -> tuple[dict | None, dict | None]:
    """ALL paths converge here. 100% shared logic:
    1. resolve_level_up_signal()  — calls game_state.level_from_xp()
    2. ensure_rewards_box()       — merge raw + state-derived
    3. ensure_planning_block()    — atomic with rewards_box
    4. normalize_rewards_box()    — clean types
    5. should_show_rewards_box()  — final visibility gate
    6. _enforce_atomicity()       — if either is None, both become None
    Returns (rewards_box, planning_block) or (None, None).
    Note: atomicity is enforced at the return boundary (step 6), not as a
    separate pass. Steps 2-3 build the pair; step 6 guarantees the invariant.
    """
```

### Private Helpers (moved from world_logic.py and game_state.py)

```python
_is_state_flag_true(value)          # ONE version, consolidated
_is_state_flag_false(value)         # ONE version
_extract_xp_robust(player_data)     # replaces 3 copy-paste blocks
_extract_level_up_loot(pending)     # from world_logic
_build_rewards_box_from_pending()   # from world_logic
_check_and_set_level_up_pending()   # from #6262
_infer_target_from_xp()            # from world_logic
_is_asi_level(level)               # from #6263
_enforce_atomicity()               # rewards_box + planning_block always paired
```

## Renamed File: `llm_parser.py` (from `streaming_orchestrator.py`)

### Why rename

`streaming_orchestrator.py` implies streaming-only. The file already handles both streaming and non-streaming LLM response parsing. The rename to `llm_parser.py` reflects its actual role: parse LLM responses, orchestrate the computation pipeline, handle persistence and response delivery.

### What moves INTO llm_parser.py from world_logic.py

The non-streaming orchestration currently in `world_logic.process_action_unified()` moves into llm_parser.py. Specifically:
- LLM call dispatch (currently calls `llm_service.continue_story`)
- Response parsing (extract structured_fields from LLM output)
- Post-LLM pipeline orchestration (game_state → rewards_engine → world_logic.inject_modal_state)
- Persistence (Firestore write of story entry + game state)
- Response assembly (build unified_response dict)

### What stays in world_logic.py

- `inject_modal_state()` — thin wrapper that adds modal flags to pre-computed payload
- `_maybe_trigger_level_up_modal()` — reads pre-computed flags, no computation
- `_inject_modal_finish_choice_if_needed()` — injects into planning_block
- `_enforce_character_creation_modal_lock()`
- `inject_persisted_living_world_fallback()`
- Planning block assembly (adventure hooks, living world)
- Story entry formatting

world_logic.py becomes a **pure consumer** — it receives pre-computed rewards data and wraps it with modal semantics. It does NOT call game_state for XP or rewards_engine for detection.

**Boundary between engine and world_logic on planning_block**: `rewards_engine.ensure_planning_block()` builds the canonical level-up structure (ASI choices, ability scores, class features). `world_logic._inject_levelup_choices_if_needed()` adds modal flavor, non-level-up hooks (adventure hooks, living world), and UI lock semantics. Engine = canonical data, world_logic = presentation/modal wrapping. Neither should duplicate ASI rows.

### What llm_parser.py does NOT do

- XP math (delegates to game_state.py)
- Rewards detection/building/normalization (delegates to rewards_engine.py)
- Modal injection (delegates to world_logic.py)
- Boolean coercion or visibility decisions (rewards_engine handles this)

## game_state.py Boundary

`game_state.py` owns:
- **Firestore I/O** (`GameState` class — read/write campaign state)
- **D&D 5e XP math** (`level_from_xp`, `xp_needed_for_level`, `xp_to_next_level`)
- **XP extraction** (`extract_character_xp` — robust multi-path read from player_data)
- **Dataclasses** (`LevelProgressionState`, `PendingRewardsState`)
- **Persisted state fields** including `level_up_pending`, `level_up_in_progress`, `level_up_available`

`game_state.py` does NOT:
- Interpret flags for UI/routing decisions (that's rewards_engine)
- Build rewards_box or planning_block (that's rewards_engine)
- Decide show/hide visibility (that's rewards_engine)
- Orchestrate the pipeline (that's llm_parser)

The distinction: game_state stores and reads `level_up_pending=True` as raw data. rewards_engine interprets what that flag means for the user experience.

## File Responsibility Changes

| File | Before | After |
|------|--------|-------|
| **llm_parser.py** | streaming_orchestrator.py (streaming only, inline level-up canonicalization) | ONE orchestration root for streaming + non-streaming + polling. Calls each layer once. |
| **rewards_engine.py** | (new) | ALL rewards/progression decisions: detection, rewards building, atomicity, normalization, visibility |
| **game_state.py** | XP math + `resolve_level_up_signal` + `ensure_level_up_rewards_pending` + `_is_state_flag_true` (3 copies) | XP math + Firestore I/O. Signal/rewards functions deprecated, redirect to engine |
| **world_logic.py** | 25+ level-up functions (~1200 lines) + non-streaming orchestration | Thin modal wrapper. Receives pre-computed payload, injects modal state. Does NOT orchestrate. |
| **agents.py** | 110-line `_is_character_creation_or_level_up_active` with own flag-reading | 3-line delegate: `return rewards_engine.is_level_up_active(game_state)` |
| **constants.py** | Duplicate `get_xp_for_level` / `get_level_from_xp` | DELETE duplicates, import from game_state |
| **app.js** | Re-coerces `level_up_available` booleans | Pure render — server guarantees clean types |

## Single Responsibility Table

| File | ONE Job | What It Does NOT Do |
|------|---------|---------------------|
| `llm_parser.py` | Parse LLM response + orchestrate pipeline + persistence + delivery | No XP math, no rewards detection/building, no modal logic, no boolean coercion |
| `game_state.py` | D&D 5e XP math + Firestore I/O + persisted state fields | No flag interpretation for UI, no rewards building, no show/hide decisions |
| `rewards_engine.py` | ALL rewards/progression decisions: detect, build, normalize, decide | No XP math, no Firestore I/O, no story entries, no modal state, no agent routing |
| `world_logic.py` | Thin modal wrapper — inject modal state into pre-computed payload | No rewards detection/building (receives from engine), no XP math, no orchestration |
| `agents.py` | Pick the right agent | No flag reading, no stale detection, no XP extraction |
| `app.js` | Render server-decided payload | No boolean coercion, no visibility decisions |

### Dependency Direction (imports flow DOWN)

```
game_state.py              ← owns XP math + Firestore I/O + flag storage
    ▲
    │ imports
    │
rewards_engine.py          ← owns flag interpretation + rewards decisions
    ▲
    │ imports
    │
llm_parser.py              ← ONE orchestration root (streaming + non-streaming + polling)
world_logic.py             ← thin modal wrapper (called BY llm_parser)
agents.py                  ← routing consumer
```

## Duplications Eliminated

| Duplication | Current | After |
|-------------|---------|-------|
| `_is_state_flag_true` | 3 versions (game_state, world_logic, agents inline) | 1 in rewards_engine (or game_state if circular import) |
| `resolve_level_up_signal` | game_state.py + world_logic._resolve_level_up_signal | 1 in rewards_engine |
| XP extraction | 3 copy-paste blocks in `_synthesize_generic_rewards_box` | 1 `_extract_xp_robust` |
| Level-up detection | agents.py (110 lines) + game_state + world_logic | 1 `is_level_up_active()` |
| XP math | constants.py + game_state.py | game_state.py only |
| `_extract_current_xp` | agents.py + game_state.py | game_state.py only |
| Show/hide decision | world_logic + app.js | 1 `should_show_rewards_box()` |
| Rewards postcondition | world_logic (non-stream) + streaming_orchestrator (stream) | 1 `canonicalize_rewards()` called by llm_parser for BOTH paths |

## Known Bugs in PRs #6262-#6268 (all fixed in clean rewrite)

| Bug | PRs affected | Fix in rewards_engine |
|-----|-------------|----------------------|
| Off-by-one: `target_level = current_level + 1` when `level_up_complete=True` — level already incremented | #6262, #6263, #6264 | `resolve_level_up_signal` checks `level_up_complete` flag before incrementing |
| Wrong dict keys: `"target_level"` / `"level"` instead of `"resolved_target_level"` / `"stored_level"` | #6262 | Consistent key names throughout engine |
| Dead function: `ensure_level_up_planning_block` (~110 lines, never called) | #6264 | `ensure_planning_block()` is always called atomically with `ensure_rewards_box()` |
| Missing `freeze_time: True` on synthesized stuck-completion choices | #6263, #6264 | Set in `ensure_planning_block()` when synthesizing |
| ASI injection checks `current_level` instead of `new_level` (target level) | #6263 | `_is_asi_level(target_level)` not `_is_asi_level(current_level)` |
| `inject_persisted_living_world_fallback` TypeError from signature change | #6264 | world_logic.py signature stabilized; llm_parser calls with correct args |

## PR Strategy

1. Close PRs #6262, #6263, #6264, #6268 with comment linking to this design
2. Cherry-pick test files from #6263/#6264 (test_level_up_asi_injection.py, test_level_up_atomicity.py, test_level_up_stale_flags.py)
3. One clean PR against main (`feat/rewards-engine-single-responsibility`)
4. Estimated net: +800 lines (new engine + llm_parser changes) / -1200 lines (removed from world_logic/game_state/agents) = -400 net

### Implementation Order (TDD + 4-Layer)

**Methodology**: RED → GREEN → WIRE → CLEAN. Tests first, implementation second, integration third, cleanup last. Each layer has a clear entry/exit gate.

**Ordering flexibility**: The layer sequence is strict (0→1→2→3), but within each layer the sub-steps are negotiable as long as the single-call-site invariant holds at each merge point. For example, Layer 1 can create `rewards_engine.py` before or after `git mv streaming_orchestrator.py → llm_parser.py` — what matters is that each commit keeps all existing tests green.

#### Parallelism Map

```
TIME →
─────────────────────────────────────────────────────────────────────

Layer 0 (RED):  ┌─ Agent A: tests 1-3 (atomicity, purity, XP boundary) ─┐
                ├─ Agent B: tests 4-5 (convergence, level/XP check)     ─┤ SYNC
                └─ Agent C: tests 6-8 (ASI, zero XP, arch invariant)    ─┘
                                                                         │
                                                        ╔════════════════╧══╗
                                                        ║ GATE: 8 FAIL 0 PASS ║
                                                        ╚════════════════╤══╝
                                                                         │
Layer 1 (GREEN): ┌─ Agent D: git mv + import fixup ──────────────────────┤
                 │  (blocker — must land first)                          │
                 └─ Agent E: rewards_engine.py (full file) ──────────────┤
                    (can START writing while D runs — no import dep yet) │
                                                                         │
                    ╔═ OVERLAP: write Layer 2 integration tests (RED) ═╗ │
                    ║ Agent F: test_streaming_single_canonicalize      ║ │
                    ║ Agent G: test_nonstreaming_single_canonicalize   ║ │
                    ║ Agent H: test_polling_project_level_up_ui        ║ │
                    ╚══════════════════════════════════════════════════╝ │
                                                                         │
                                                        ╔════════════════╧══╗
                                                        ║ GATE: 8 PASS 0 FAIL ║
                                                        ╚════════════════╤══╝
                                                                         │
Layer 2 (WIRE):  ┌─ Agent I: streaming path (llm_parser.py) ────────────┐
                 ├─ Agent J: non-streaming path (llm_parser.py) ────────┤
                 ├─ Agent K: polling path (llm_parser.py) ──────────────┤
                 ├─ Agent L: game_state.py deprecation redirects ───────┤
                 │  (independent — different file)                       │
                 └─ AFTER I+J+K: Agent M: world_logic.py strip ─────────┤ SYNC
                                                                         │
                                                        ╔════════════════╧══╗
                                                        ║ GATE: all tests green ║
                                                        ║ single-call-site ✓    ║
                                                        ╚════════════════╤══╝
                                                                         │
Layer 3 (CLEAN): ┌─ Agent N: delete _is_state_flag_true (3 files) ──────┐
                 ├─ Agent O: delete constants.py XP dupes ──────────────┤
                 ├─ Agent P: agents.py 110→3 lines ─────────────────────┤ ALL
                 ├─ Agent Q: app.js boolean cleanup ────────────────────┤ PARALLEL
                 └─ Agent R: remove deprecation redirects ──────────────┘
                                                                         │
                                                        ╔════════════════╧══╗
                                                        ║ GATE: net negative   ║
                                                        ║ lines, CI green      ║
                                                        ╚══════════════════════╝
```

**Max parallelism by layer:**
| Layer | Max concurrent agents | Bottleneck |
|-------|----------------------|------------|
| 0 (RED) | 3 | None — tests are independent functions |
| 1 (GREEN) | 2 + 3 overlap | git mv must land before rewards_engine.py imports work; Layer 2 tests can be written in parallel (RED) |
| 2 (WIRE) | 4, then 1 | I/J/K touch same file (llm_parser.py) — need coordinated sections or sequential merge. L is independent. M waits on I+J+K. |
| 3 (CLEAN) | 5 | None — all touch different files |

**Critical path**: Layer 2 is the bottleneck. Agents I/J/K all modify `llm_parser.py` — they can work on separate functions but must merge sequentially to avoid conflicts. Alternative: one agent handles all three llm_parser paths while Agent L handles game_state redirects in parallel.

**Overlap opportunity**: Layer 2 integration tests (RED) can be written DURING Layer 1 implementation. This saves one full cycle — by the time Layer 1 is done, Layer 2 tests already exist and are failing, ready for the wiring agents to make them green.

#### Layer 0: RED — Contract Tests (bead `rev-v4t0`)

Write FAILING tests that define the `rewards_engine.py` contract. These tests run against the current codebase and MUST FAIL (proving the contract isn't yet satisfied).

```
Test file: mvp_site/tests/test_rewards_engine.py

Tests to write (all RED on current main):

1. test_canonicalize_returns_atomic_pair
   - canonicalize_rewards() returns (rb, pb) where both non-None, or (None, None)
   - NEVER (rb, None) or (None, pb)

2. test_project_level_up_ui_is_pure
   - Same game_state_dict → same output, 100 calls
   - No Firestore writes (mock Firestore, assert 0 writes)

3. test_resolve_level_up_signal_xp_boundary
   - XP exactly at threshold (300, 900, 2700, ...) → level_up detected
   - XP at threshold-1 → no level_up

4. test_canonicalize_core_convergence
   - Given identical game_state, streaming path and polling path
     produce identical (rewards_box, planning_block) output

5. test_level_xp_consistency_check
   - stored_level=3, current_xp=250 (level 1 XP) → warning logged,
     XP-derived level used for threshold calc

6. test_concurrent_asi_rewards
   - Fighter reaching level 6 + Rogue reaching level 10 in same action
   - Both ASI choices present in single rewards_box

7. test_zero_xp_is_noop
   - xp_gained=0 → no rewards_box emitted, no level-up triggered

8. test_single_call_site_invariant (architectural)
   - grep llm_parser.py for canonicalize_rewards → exactly 1 call site
   - grep llm_parser.py for project_level_up_ui → exactly 1 call site
   - grep world_logic.py for canonicalize_rewards → 0 call sites
```

**Entry gate**: Design doc approved (done).
**Exit gate**: All tests exist, all FAIL on current main. `pytest test_rewards_engine.py` = 8 FAIL, 0 PASS.

#### Layer 1: GREEN — Pure Implementation (bead `rev-v4t1`)

Implement `rewards_engine.py` with minimal code to make Layer 0 tests pass. No wiring to `llm_parser.py` yet — pure functions only.

```
1. git mv streaming_orchestrator.py → llm_parser.py + update imports
2. Create rewards_engine.py:
   - _canonicalize_core() — THE shared computation
   - canonicalize_rewards() — streaming + non-streaming entry
   - project_level_up_ui() — polling entry
   - resolve_level_up_signal() — moved from game_state
   - ensure_rewards_box() + ensure_planning_block() — atomic pair
   - normalize_rewards_box() — type cleaning
   - should_show_rewards_box() — visibility gate
   - is_level_up_active() — consolidated detector
   - _is_state_flag_true() — ONE version (3→1)
   - Level/XP consistency check with warning log
3. Run test_rewards_engine.py → 8 PASS, 0 FAIL
```

**Entry gate**: Layer 0 tests all FAIL.
**Exit gate**: Layer 0 tests all PASS. `rewards_engine.py` has no imports from `llm_parser` or `world_logic`. Strict one-way: `rewards_engine → game_state` only.

#### Layer 2: WIRE — Integration (bead `rev-v4t2`)

Wire `llm_parser.py` to call `rewards_engine`. Move non-streaming orchestration from `world_logic`. Strip `world_logic` to thin modal wrapper.

```
1. llm_parser.py streaming path:
   - Replace inline canonicalization with rewards_engine.canonicalize_rewards()
   - Single call site, result used for both persist + SSE done event

2. llm_parser.py non-streaming path:
   - Move process_action_unified orchestration from world_logic
   - Replace DOUBLE canonicalization with single rewards_engine.canonicalize_rewards()

3. llm_parser.py polling path:
   - Replace _project_level_up_ui_from_game_state with rewards_engine.project_level_up_ui()

4. world_logic.py:
   - Keep inject_modal_state(), _inject_modal_finish_choice_if_needed(), etc.
   - Remove all rewards detection/building/normalization functions
   - Add deprecation redirects for moved functions

5. game_state.py:
   - resolve_level_up_signal → thin redirect with deprecation warning
   - ensure_level_up_rewards_pending → thin redirect

Integration tests:
   - test_streaming_path_uses_single_canonicalize()
   - test_nonstreaming_path_uses_single_canonicalize()
   - test_polling_path_uses_project_level_up_ui()
   - test_no_double_canonicalization() — grep for 2nd call site, assert 0
```

**Entry gate**: Layer 1 complete (all pure tests green).
**Exit gate**: All existing tests pass. Integration tests pass. `grep -c canonicalize_rewards llm_parser.py` = 1. `grep -c canonicalize_rewards world_logic.py` = 0.

#### Layer 3: CLEAN — Delete + Simplify (bead `rev-v4t3`)

```
1. Delete 3 copies of _is_state_flag_true (game_state, world_logic, agents inline)
2. Delete duplicate XP math from constants.py
3. agents.py: 110-line _is_character_creation_or_level_up_active → 3-line delegate
4. app.js: Remove boolean coercion (server guarantees types)
5. Remove deprecation redirects after confirming no callers
6. Run full test suite — all green
```

**Entry gate**: Layer 2 complete (integration tests green).
**Exit gate**: `git diff --stat` shows net negative lines. Full CI green. No duplicate functions remain (`grep -r _is_state_flag_true` → 1 result in rewards_engine.py only).

---

### Legacy Implementation Order (superseded by TDD layers above)

1. ~~`git mv streaming_orchestrator.py llm_parser.py` + update all imports~~
2. ~~Create `rewards_engine.py` with full public API~~
3. ~~Wire llm_parser.py to call rewards_engine~~
4. ~~Move non-streaming orchestration from world_logic.py into llm_parser.py~~
5. ~~Strip world_logic.py to thin modal wrapper~~
6. ~~Update agents.py to delegate to rewards_engine~~
7. ~~Delete duplicate XP math from constants.py~~
8. ~~Clean app.js boolean coercion~~

## Migration Safety

- `game_state.resolve_level_up_signal` kept as thin redirect with deprecation warning for one release
- `game_state.ensure_level_up_rewards_pending` same treatment
- `world_logic.normalize_rewards_box_for_ui` same treatment
- All redirects removed in follow-up PR after callers confirmed migrated

## Future: world_logic.py scope reduction

After this PR, world_logic.py still owns non-rewards orchestration (story formatting, adventure hooks, living world). A follow-up could further split it, but that's out of scope for this PR.

---

## Detailed Flow Diagrams

### CURRENT: Three Separate Code Paths (Today)

#### Path A: Streaming (`streaming_orchestrator.py:532`)

```
main.py: POST /api/campaigns/<id>/interaction/stream
  └─ streaming_orchestrator.stream_story_with_game_state()         ← ROOT
       │
       ├─ firestore_service.get_campaign_by_id()                   load campaign
       ├─ firestore_service.get_campaign_game_state()              load state
       ├─ firestore_service.get_user_settings()                    load settings
       ├─ world_logic._maybe_trigger_level_up_modal()              modal pre-check
       │
       ├─ llm_service.continue_story_streaming()                   LLM call (yields events)
       │   └─ for event in stream:
       │       └─ on "done" event:
       │
       │   ┌── STATE PERSISTENCE ────────────────────────────────
       │   ├─ pre_response_state_dict = snapshot                   original state
       │   ├─ world_logic._enforce_character_creation_modal_lock() modal lock
       │   ├─ firestore_service.update_state_with_changes()        merge state_updates
       │   │
       │   ├─ world_logic._resolve_canonical_level_up_ui_pair()    ← REWARDS CANON (40 lines inline)
       │   │   ├─ calls _has_level_up_ui_signal()
       │   │   ├─ calls _planning_has_level_up_choices()
       │   │   └─ decides suppress/keep/rewrite
       │   │
       │   ├─ world_logic._inject_modal_finish_choice_if_needed()  modal finish
       │   ├─ world_logic._increment_turn_counter()                turn tracking
       │   ├─ world_logic._maybe_update_living_world_tracking()    living world
       │   ├─ firestore_service.update_campaign_game_state()        ← PERSIST STATE
       │   └── END STATE ────────────────────────────────────────
       │
       │   ┌── STORY PERSISTENCE ────────────────────────────────
       │   ├─ parse_structured_response()                          validate narrative
       │   ├─ firestore_service.add_story_entry("user", ...)       persist user entry
       │   ├─ _enrich_streaming_structured_fields()                backfill living world
       │   ├─ world_logic._inject_modal_finish_choice_if_needed()  modal finish (2nd call!)
       │   ├─ Apply canonical_stream_rewards_box to gemini_structured
       │   ├─ firestore_service.add_story_entry("gemini", ...)     ← PERSIST STORY
       │   └── END STORY ────────────────────────────────────────
       │
       ├─ yield done event (SSE)                                   → app.js
       └─ yield persistence_warnings
```

#### Path B: Non-Streaming (`world_logic.py:5553`)

```
main.py: POST /api/campaigns/<id>/action
  └─ world_logic.process_action_unified()                          ← ROOT
       │
       ├─ _prepare_game_state_with_user_settings()                 load state + settings
       ├─ _is_god_mode_return_to_story()                           god mode check
       │
       ├─ _load_campaign_and_continue_story()                      LLM call (blocking)
       │   └─ llm_service.continue_story()
       │
       ├─ preventive_guards.enforce_preventive_guards()            state guards
       ├─ _enforce_character_creation_modal_lock()                 modal lock
       ├─ _apply_timestamp_to_world_time()                         time normalization
       ├─ world_time.ensure_progressive_world_time()               time validation
       │
       ├─ original_state_for_level_check = deep_copy snapshot      ← ORIGINAL STATE
       ├─ update_state_with_changes()                              merge state_updates
       │
       ├─ _detect_rewards_discrepancy()                            rewards validation
       ├─ _enforce_primary_rewards_box_postcondition() ×2          ← REWARDS (1st + 2nd call)
       ├─ ensure_level_up_rewards_pending()                        ← LEVEL-UP DETECTION
       ├─ validate_and_correct_state()                             state validation
       │
       ├─ _increment_turn_counter()                                turn tracking
       ├─ _maybe_update_living_world_tracking()                    living world
       │
       ├─ structured_fields = extract_structured_fields()          parse LLM output
       ├─ normalize_rewards_box_for_ui()                           ← NORMALIZE (1st)
       │
       │   ┌── LEVEL-UP CANONICALIZATION ────────────────────────
       │   ├─ _should_emit_level_up_rewards_box()                  emit check
       │   ├─ _inject_levelup_choices_if_needed()                  choice injection
       │   ├─ _resolve_canonical_level_up_ui_pair()                ← CANON PAIR
       │   ├─ _inject_campaign_upgrade_choice_if_needed()          upgrade injection
       │   ├─ _inject_levelup_narrative_if_needed()                narrative injection
       │   ├─ _inject_spicy_mode_choice_if_needed()                spicy injection
       │   └─ _inject_modal_finish_choice_if_needed()              modal finish
       │   └── END CANON ────────────────────────────────────────
       │
       ├─ _persist_turn_to_firestore()                             ← PERSIST
       │
       │   ┌── RESPONSE BUILDING ────────────────────────────────
       │   ├─ normalize_rewards_box_for_ui()                       ← NORMALIZE (2nd!)
       │   ├─ _enforce_rewards_box_planning_atomicity()            ← ATOMICITY
       │   ├─ _inject_campaign_upgrade_choice_if_needed()          ← 2nd call!
       │   ├─ _inject_levelup_narrative_if_needed()                ← 2nd call!
       │   ├─ _inject_spicy_mode_choice_if_needed()                ← 2nd call!
       │   ├─ _inject_modal_finish_choice_if_needed()              ← 2nd call!
       │   └── END RESPONSE ─────────────────────────────────────
       │
       └─ return unified_response dict                             → app.js
```

#### Path C: Polling (`world_logic.py:7501`)

```
main.py: GET /api/campaigns/<id>
  └─ world_logic.get_campaign_state_unified()                      ← ROOT
       │
       ├─ firestore_service.get_campaign_by_id()                   load campaign
       ├─ _prepare_game_state_with_user_settings()                 load state
       │
       ├─ _extract_latest_gemini_ui_fields(story)                  read stored rewards
       │
       ├─ If no stored rewards:
       │   └─ _project_level_up_ui_from_game_state()               ← RE-DERIVE
       │
       ├─ _should_emit_level_up_rewards_box()                      stale check
       ├─ _enforce_rewards_box_planning_atomicity()                ← ATOMICITY
       ├─ _inject_modal_finish_choice_if_needed()                  modal finish
       │
       └─ return result dict                                       → app.js
```

---

### TARGET: v4 Single-Root Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│ llm_parser.py (renamed streaming_orchestrator.py)     ← SINGLE ROOT│
│                                                                     │
│  Three entry points, ONE pipeline:                                  │
│   • stream_and_process()     ← streaming POST                      │
│   • process_action()         ← non-streaming POST (main.py calls    │
│   │                            llm_parser directly; world_logic is  │
│   │                            thin façade only for modal injection) │
│   • get_campaign_state()     ← polling GET (main.py calls           │
│                                llm_parser directly)                  │
│                                                                     │
│  ALL three call the same downstream sequence:                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ 1. Load state + settings (Firestore)                         │   │
│  │ 2. Call LLM (streaming or blocking)  [skip for polling]      │   │
│  │ 3. Parse structured_fields                                   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ game_state.py: XP math                              Stage 2  │   │
│  │  • extract_character_xp(player_data)                         │   │
│  │  • level_from_xp(xp) → level                                │   │
│  │  • xp_needed_for_level(level) → threshold                    │   │
│  │  • LevelProgressionState dataclass                           │   │
│  │  • Firestore I/O (get/update campaign state)                 │   │
│  │                                                               │   │
│  │  Does NOT: interpret flags, build rewards, decide visibility  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ rewards_engine.py: canonicalize                   Stages 3-4 │   │
│  │                                                               │   │
│  │  ONE call per request:                                        │   │
│  │   canonicalize_rewards(structured_fields, game_state_dict,    │   │
│  │                        original_state_dict)                   │   │
│  │   OR                                                          │   │
│  │   project_level_up_ui(game_state_dict)  [polling only]        │   │
│  │                                                               │   │
│  │  Both converge on _canonicalize_core():                       │   │
│  │   1. resolve_level_up_signal()     — ONE detector             │   │
│  │   2. ensure_rewards_box()          — atomic with planning     │   │
│  │   3. ensure_planning_block()       — atomic with rewards      │   │
│  │   4. normalize_rewards_box()       — clean types              │   │
│  │   5. should_show_rewards_box()     — visibility gate          │   │
│  │   6. _enforce_atomicity()          — pair or (None, None)     │   │
│  │                                                               │   │
│  │  Returns: (rewards_box, planning_block) or (None, None)       │   │
│  │                                                               │   │
│  │  Also owns:                                                   │   │
│  │   is_level_up_active()             — agents.py delegate       │   │
│  │   _is_state_flag_true/false()      — ONE version              │   │
│  │   _extract_xp_robust()            — ONE version               │   │
│  │   _is_asi_level(level)            — Fighter/Rogue/other       │   │
│  │                                                               │   │
│  │  Does NOT: Firestore I/O, modal logic, story entries          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ world_logic.py: modal wrap                          Stage 5  │   │
│  │                                                               │   │
│  │  inject_modal_state(rewards_box, planning_block, game_state)  │   │
│  │   • _inject_modal_finish_choice_if_needed()                   │   │
│  │   • _inject_campaign_upgrade_choice_if_needed()               │   │
│  │   • _inject_spicy_mode_choice_if_needed()                     │   │
│  │   • _inject_levelup_narrative_if_needed()                     │   │
│  │   • _enforce_character_creation_modal_lock()                  │   │
│  │   • inject_persisted_living_world_fallback()                  │   │
│  │                                                               │   │
│  │  Receives pre-computed (rb, pb) — wraps with modal flags.     │   │
│  │  Does NOT call game_state or rewards_engine.                  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ Persist to Firestore                                Stage 6  │   │
│  │  • update_campaign_game_state()                               │   │
│  │  • add_story_entry("user", ...)                               │   │
│  │  • add_story_entry("gemini", ..., structured_fields)          │   │
│  └──────────────────────────────────────────────────────────────┘   │
│         │                                                           │
│         ▼                                                           │
│  Return to frontend:                                     Stage 7   │
│   • Streaming: yield SSE done event → app.js                       │
│   • Non-streaming: return unified_response → app.js                │
│   • Polling: return campaign state → app.js                        │
│                                                                     │
│  app.js: if (fullData.rewards_box) { renderRewardsBox(rb); }       │
│  Server guarantees: bools are bool, ints are int, null when hidden  │
└─────────────────────────────────────────────────────────────────────┘
```

---

### What Moves Where

| Current Location | Function | Destination |
|---|---|---|
| `world_logic.py` | `_resolve_canonical_level_up_ui_pair()` | `rewards_engine._canonicalize_core()` |
| `world_logic.py` | `_project_level_up_ui_from_game_state()` | `rewards_engine.project_level_up_ui()` |
| `world_logic.py` | `_enforce_rewards_box_planning_atomicity()` | `rewards_engine._enforce_atomicity()` |
| `world_logic.py` | `_should_emit_level_up_rewards_box()` | `rewards_engine.should_show_rewards_box()` |
| `world_logic.py` | `_has_level_up_ui_signal()` | `rewards_engine.resolve_level_up_signal()` |
| `world_logic.py` | `normalize_rewards_box_for_ui()` | `rewards_engine.normalize_rewards_box()` |
| `world_logic.py` | `_enforce_primary_rewards_box_postcondition()` | `rewards_engine` (absorbed into canonicalize) |
| `world_logic.py` | `_inject_levelup_choices_if_needed()` | stays in `world_logic` (modal injection) |
| `world_logic.py` | `process_action_unified()` orchestration | `llm_parser.py` |
| `world_logic.py` | `get_campaign_state_unified()` orchestration | `llm_parser.py` |
| `game_state.py` | `resolve_level_up_signal()` | `rewards_engine` (thin redirect stays) |
| `game_state.py` | `ensure_level_up_rewards_pending()` | `rewards_engine` (thin redirect stays) |
| `game_state.py` | `_is_state_flag_true()` | `rewards_engine` (ONE version) |
| `agents.py` | `_is_character_creation_or_level_up_active()` (110 lines) | 3-line delegate to `rewards_engine.is_level_up_active()` |

**Key insight**: The non-streaming path calls rewards normalization/canonicalization/atomicity TWICE — once for Firestore persistence (lines 6808-6882) and again for the response (lines 7250-7317). The streaming path has the same double-touch pattern. The v4 design eliminates this: rewards_engine returns the canonical pair ONCE, and that single result is used for both persistence and response.

---

## Multi-Model Review Assessment (2026-04-14)

**Source**: Secondo analysis (Cerebras/Qwen3, Gemini 3 Flash, Perplexity Sonar Pro)

### Accepted (already handled in codebase)

| Finding | Status | Evidence |
|---|---|---|
| SRP separation correct | ✅ Confirmed | All 3 models agree |
| Double-touch bug correctly diagnosed | ✅ Confirmed | v4 eliminates by single-call-site design |
| Zero/negative XP guard needed | ✅ Already exists | `game_state.py:853` clamps negative→0, `:1503` `max(0, xp_gained)`, `:3063-3076` validation clamp |
| Level cap 20 enforcement | ✅ Already exists | `game_state.py:891` `max(1, min(20, level))`, `:928` returns 0 at level 20, `level_from_xp()` structurally caps |
| Streaming partial JSON handling | ✅ Already exists | `streaming_orchestrator.py` (→`llm_parser.py`) accumulates tokens, parses only complete JSON |

### Adapted (design invariant added)

| Finding | Action |
|---|---|
| Rapid polling idempotency | `project_level_up_ui()` MUST remain pure/read-only — no Firestore writes on poll path. Design invariant, not a code guard. |
| Concurrent ASI rewards (Fighter@6, Rogue@10) | Add unit test in `rev-v4s2` for multi-ASI scenarios in single rewards_box. `_canonicalize_core()` handles this via single pass. |

### Adapted (multiclass)

| Finding | Action |
|---|---|
| Multiclass XP (`total_level = sum(class_levels)`) | LLM can narrate multiclassing (e.g. "Fighter 3 / Rogue 2"). Schema has single `level` field = total character level. Risk: LLM sets `level` to class level instead of total. Add sanity check in `_canonicalize_core()` that `level` is consistent with XP (i.e. `level_from_xp(current_xp) == level`). If mismatch, log warning and use XP-derived level. |

### Rejected

| Finding | Reason |
|---|---|
| "experience_overflow" flag in migration table | Hallucinated — no such field exists in codebase |
| "DeferredRewardsProtocol" as server-side protocol | Not a server-side protocol or schema object — prompt-only. The concept exists as an LLM instruction, not as a Python class or formal protocol. System uses plain dicts + PendingRewardsState dataclass. |
| "canonicalisation_version" / SHA-256 checksum | Over-engineering — single-call-site makes re-canonicalization structurally impossible |
| XSS in modal text | Already mitigated (Flask/Jinja2 auto-escape + vanilla JS text insertion). Out of scope for rewards engine. |

### Design Invariants (from this review)

1. **`project_level_up_ui()` is pure**: No side effects, no Firestore writes. Same input → same output. Polling path is read-only.
2. **Single call site is the XSS/idempotency/double-touch guard**: The architecture itself prevents these classes of bugs. Additional runtime guards (checksums, version fields, TTL hashes) are unnecessary.
