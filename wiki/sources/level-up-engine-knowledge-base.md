# Level-Up Engine Knowledge Base

**Type**: source
**Tags**: [level-up, rewards-engine, architecture, knowledge-base, worldarchitect]
**Date**: 2026-04-14
**Status**: Active — PR #6276 OPEN, PR #6273 DEPLOYED with regression

---

## Purpose

This doc is the **single source of truth** for the level-up engine's requirements, code architecture, and open issues. It exists to prevent drift between design intent and implementation. Update it whenever a PR changes the engine.

---

## 1. Requirements (What the Engine Must Do)

### 1.1 Core Responsibilities

The rewards engine (`rewards_engine.py`) has ONE job: **all rewards/progression decisions**.

| Responsibility | Description |
|---|---|
| Detect | Determine if a level-up is warranted (XP threshold crossing) |
| Build | Construct `rewards_box` + `planning_block` pair |
| Normalize | Guarantee clean types (bool, int) |
| Decide Visibility | Determine if `rewards_box` should be shown to user |
| **NOT its job** | XP math (→ `game_state`), Firestore I/O (→ `llm_parser`), modal injection (→ `world_logic`) |

### 1.2 Visibility Rules

`should_show_rewards_box()` returns True when:
- `level_up_available=True` (active level-up in progress), OR
- `xp_gained > 0` (XP progress toward next level, e.g. `xp=350/900`)

**Critical**: XP-progress without level-up (`xp_gained > 0` but `level_up_available=False`) MUST emit a `rewards_box`. This was the v3 semantic. The v4 regression suppressed this.

### 1.3 Atomicity Contract

`rewards_box` and `planning_block` are **atomic** — if either is None, both must be None. This is enforced by `_enforce_atomicity()` at the return boundary.

Exception: XP-progress-only (no level-up) is **non-atomic** — `planning_block` is None but `rewards_box` alone is valid.

### 1.4 Single-Call Invariant

Each request calls `rewards_engine` **once** via exactly one entry point:

| Path | Entry Point | Location |
|---|---|---|
| Streaming + Non-streaming | `canonicalize_rewards()` | `llm_parser.py:717` |
| Polling | `project_level_up_ui()` | `llm_parser.py:617` |

After that call, no file re-enters the pipeline. No re-canonicalization.

### 1.5 Dependency Direction

```
game_state.py (XP math + flag storage)
         ▲
         │ imports
         │
rewards_engine.py (flag interpretation + rewards decisions)
         ▲
         │ imports
         │
llm_parser.py ──→ world_logic.py ──→ app.js (render only)
```

`game_state.py` does **NOT** import `rewards_engine.py`. Strict one-way dependency.

### 1.6 7-Stage Pipeline

| Stage | File | Responsibility |
|---|---|---|
| 1. FETCH+PARSE | `llm_parser.py` | Parse LLM response → structured fields |
| 2. XP MATH | `game_state.py` | Level, XP numbers |
| 3. DETECT+BUILD | `rewards_engine.py` | `rewards_box`, `planning_block` |
| 4. NORMALIZE | `rewards_engine.py` | Clean types, `should_show` |
| 5. MODAL+STORY | `world_logic.py` | Modal injection, story assembly |
| 6. PERSIST | `llm_parser.py` | Firestore write |
| 7. RENDER | `app.js` | Pure render, zero logic |

---

## 2. Code Architecture (Current State)

### 2.1 File Inventory

| File | Lines | Role |
|---|---|---|
| `mvp_site/rewards_engine.py` | 484 | Single source of truth for rewards/progression decisions |
| `mvp_site/world_logic.py` | 8644 | Orchestration + modal injection (NOT thin wrapper — see §3) |
| `mvp_site/llm_parser.py` | 1035 | Streaming orchestrator + non-streaming + polling |
| `mvp_site/game_state.py` | ~1800 | XP math, flag storage |

### 2.2 rewards_engine.py Public API (7 functions)

```python
# Signal Detection
is_level_up_active(game_state_dict) → bool                    # Line 113 — ONE detector
resolve_level_up_signal(game_state_dict, rewards_box, original_state_dict) → tuple[bool, int|None, bool]  # Line 124

# Rewards Building (atomic pair)
ensure_rewards_box(game_state_dict, structured_fields, original_state_dict) → dict|None  # Line 194
ensure_planning_block(game_state_dict, rewards_box) → dict|None  # Line 249

# UI Formatting
normalize_rewards_box(rewards_box) → dict|None  # Line 321
should_show_rewards_box(rewards_box) → bool     # Line 343

# Two Entry Points (both converge to _canonicalize_core)
canonicalize_rewards(structured_fields, game_state_dict, original_state_dict) → tuple  # Line 458
project_level_up_ui(game_state_dict) → tuple     # Line 477
```

### 2.3 world_logic.py Level-Up Functions

Despite the v4 design calling for world_logic to be a "thin modal wrapper only", these orchestration functions remain:

| Function | Line | Role |
|---|---|---|
| `_enforce_primary_rewards_box_postcondition` | 1246 | Postcondition synthesis — calls `project_level_up_ui()` at line 1275 |
| `_project_level_up_ui_from_game_state` | 1669 | Wrapper that calls `project_level_up_ui()` + atomicity enforcement |
| `_has_level_up_ui_signal` | 1695 | Wrapper calling `project_level_up_ui()` |
| `_resolve_canonical_level_up_ui_pair` | 1715 | Orchestration wrapper with injection logic |

**Design gap**: These delegate TO `rewards_engine` but are NOT just thin modal wrappers. They contain orchestration logic that was supposed to migrate into `rewards_engine`.

### 2.4 llm_parser.py Call Sites

| Line | Call | Path | Captured? |
|---|---|---|---|
| 617 | `rewards_engine.project_level_up_ui(current_game_state.to_dict())` | Polling | ✅ Yes — emitted in metadata event |
| 717 | `rewards_engine.canonicalize_rewards(structured_fields, updated_state_dict, ...)` | Streaming/Non-streaming | ✅ Yes — used for canonical stream vars |

Single-call invariant: ✅ HONORED.

---

## 3. Gap Analysis: Design vs Reality

### 3.1 v4 Design Aspirations vs PR #6276 Reality

| Design Goal | Status | Notes |
|---|---|---|
| world_logic = thin modal wrapper only | **NOT ACHIEVED** | Orchestration functions remain in world_logic (lines 1246, 1669, 1695, 1715) |
| `_resolve_canonical_level_up_ui_pair()` → `rewards_engine._canonicalize_core()` | **PARTIAL** | world_logic still calls its own wrapper |
| Single-call invariant | **ACHIEVED** ✅ | One `canonicalize_rewards` per path |
| No re-canonicalization | **ACHIEVED** ✅ | Single forward pass |
| XP-progress visibility | **REGRESSION** ❌ | `should_show_rewards_box` suppresses XP-progress (see §4.1) |
| `project_level_up_ui()` return captured | **PARTIAL** | Return captured at line 617, emitted in metadata |
| Hardcoded HP values | **STILL PRESENT** ❌ | `ensure_planning_block` uses `HIT_DICE_BY_CLASS` (partially fixed — now looks up die, not hardcoded) |

### 3.2 PR #6276 Achievements

Despite not reaching the aspirational "thin wrapper" goal, PR #6276 DID achieve:

1. ✅ CR #1: `_enforce_primary_rewards_box_postcondition` uses `project_level_up_ui()` not `is_level_up_active()`
2. ✅ CR #2: Stale finish-button suppression corrected
3. ✅ CR #3: Dead `canonical_ids` variable removed
4. ✅ CR #4: Druid added to `non_canonical_level_up_ids` allowlist
5. ✅ Key mismatch: `new_level` → `resolved_target_level` at 3 call sites
6. ✅ Real-mode E2E tests confirmed passing

---

## 4. Open Bugs

### 4.1 Bug: XP-Progress rewards_box Suppressed (CRITICAL)

**File**: `rewards_engine.py`
**Function**: `should_show_rewards_box()` (line 343) and `_canonicalize_core()` (line 378)

**Problem**: `should_show_rewards_box()` was intended to allow XP-progress boxes (`xp_gained > 0`) through. However, `_canonicalize_core()` step 5 (line 446) suppresses BOTH `rewards_box` and `planning_block` when the visibility gate returns False. For XP-progress without level-up, this means `(None, None)` is returned instead of a valid `rewards_box`.

**Root cause in code**:
```python
# rewards_engine.py line 419-422
if normalized_rb and not should_show_rewards_box(normalized_rb):
    return None, None  # ← BOTH suppressed for XP-progress case
```

But `should_show_rewards_box()` (line 343-362) actually DOES check `xp_gained > 0`. The bug may be in the merged_rb construction or the `_canonicalize_core` XP-progress branch.

**Bug introduced in**: PR #6273 (deployed)
**Fix owner**: PR #6276 or separate PR

### 4.2 Bug: project_level_up_ui Return Captured but Metadata Emit May Be Dropped

**File**: `llm_parser.py` line 617
**Problem**: `projected_rb, projected_pb` are captured and emitted in early metadata (lines 634-639), but the `if early_metadata:` guard at line 638 could drop the emit if `_build_early_metadata_payload()` returns a falsy but non-None value.

**Fix**: The fix at line 632-633 explicitly converts None to `{}` — this was the CR #1 fix.

### 4.3 Bug: Hardcoded HP Values in ensure_planning_block

**File**: `rewards_engine.py` line 266-277
**Problem**: Uses `HIT_DICE_BY_CLASS` lookup for die size, then computes `hp_value = die_size // 2 + 1`. This is correct D&D 5e average HP math, but the class lookup key is derived from `classes[0].get("class_type")` which may not match the `HIT_DICE_BY_CLASS` keys.

**Status**: Partially fixed — now uses die lookup instead of hardcoded values. Verify key matching.

---

## 5. Test Inventory

### 5.1 Real-Mode E2E Tests (no mocks, real Firebase, real LLM)

| Test File | Status | Coverage |
|---|---|---|
| `testing_mcp/test_cr1_premodal_badge_projection.py` | **PASS 1/1** | CR #1: pre-modal badge uses `project_level_up_ui()`, XP threshold crossing |
| `testing_mcp/streaming/test_level_up_streaming_e2e.py` | **PASS 2/2** | Scenario A (real XP), Scenario B (rewards_box contract) |

### 5.2 Unit Tests

| Test File | Coverage |
|---|---|
| `mvp_site/tests/test_world_logic.py` | `TestPrimaryRewardsBoxPostcondition`, `TestStaleFinishButtonSuppressionCR2`, `TestDruidInNonCanonicalLevelUpIds`, `TestPlanningHasAdvancedLevelUpChoiceDeadCode` |
| `mvp_site/tests/test_rewards_engine.py` | Layer 0 contract tests (RED phase — prove contracts unsatisfied on main) |

### 5.3 Evidence Bundles

| Test | Evidence Path |
|---|---|
| CR #1 pre-modal badge | `/tmp/worldarchitect.ai/feat_world-logic-clean-layer3/cr1_premodal_badge_projection/latest/` |
| Streaming E2E | `/tmp/worldarchitect.ai/feat_world-logic-clean-layer3/level_up_streaming_e2e/latest/` |

---

## 6. PR Status

| PR | Title | Branch | HEAD | Status |
|---|---|---|---|---|
| #6273 | feat: rewards engine single-responsibility | `feat/rewards-engine-single-responsibility` | merged | **DEPLOYED** — contains XP-progress regression |
| #6276 | feat(world_logic): Layer 3 CLEAN | `feat/world-logic-clean-layer3` | `4c2be6e98` | **OPEN** — mergeable, CR stale (unstable) |

**CR blocker on #6276**: 5 stale CodeRabbitAI CHANGES_REQUESTED (all pre-fix commits) — dismissed.

**CI status**: Green (pre-existing infra failures unrelated to PR).

---

## 7. Wiki Navigation

| Doc | Purpose |
|---|---|
| `level-up-engine-v4-design.md` | Original design doc — aspirational goals |
| `level-up-v4-current-status-2026-04-14.md` | Previous status doc (now superseded) |
| `level-up-v4-semantic-regression-bug.md` | 6 production bug analysis |
| `level-up-engine-knowledge-base.md` | **THIS DOC** — authoritative requirements + code truth |
| `rewards-system-protocol.md` | Deferred rewards protocol |

---

## 8. How to Update This Doc

When making changes to the level-up engine:

1. **Update this doc FIRST** if the change affects architecture or requirements
2. Update `rewards_engine.py` docstring header if public API changes
3. Update `level-up-v4-current-status-2026-04-14.md` for PR-level status changes
4. Update `rewards_engine.py` source comments for inline implementation details
5. **Never** let design docs and code drift without updating this doc

**Drift detection**: If `should_show_rewards_box()` semantics in code differ from §1.2, the code is wrong, not this doc.
