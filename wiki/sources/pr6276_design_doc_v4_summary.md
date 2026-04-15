---
title: "PR #6276 Design Doc v4 Summary"
type: source
tags: ["pull-request", "rewards-engine", "level-up", "refactor", "world-logic"]
source_file: "roadmap/level-up-engine-single-responsibility-design-2026-04-14.md"
date: 2026-04-14
last_updated: 2026-04-15
---

## Description
Source page for PR #6276 (feat/world-logic-clean-layer3) implementing the "Rewards Engine: Single-Responsibility Pipeline Refactor" v4 design. Design doc canonical location: `roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`.

## Architecture
Single forward pass — no file called twice, no re-canonicalization:
- Stage 1: FETCH+PARSE — `llm_parser.py` (ONE orchestration root for streaming + non-streaming + polling)
- Stage 2: XP MATH — `game_state.py`
- Stage 3: DETECT+BUILD — `rewards_engine.py` (ALL rewards/progression decisions)
- Stage 4: NORMALIZE — `rewards_engine.py`
- Stage 5: MODAL+STORY — `world_logic.py` (thin modal wrapper ~1500 lines)
- Stage 6: PERSIST — `llm_parser.py`
- Stage 7: RENDER — `app.js`

## Key Files
| File | Lines | Role |
|------|-------|------|
| `llm_parser.py` | 1060 | Single orchestration root (streaming + non-streaming + polling) |
| `rewards_engine.py` | 491 | ALL rewards/progression decisions |
| `world_logic.py` | 8729 | Thin modal wrapper (target ~1500) |
| `game_state.py` | 4387 | XP math + Firestore I/O |

## Status
- **PR #6276**: OPEN, ~75% implemented
- **All 5 CI grep gates passing** (design-doc-gate.yml)
- **Layer 3 CLEAN gap identified**: world_logic.py line count not tracked by CI gate

## Remaining Work (Layer 3 CLEAN)
1. `world_logic.py`: strip from 8729 to ~1500 lines
2. Delete `_maybe_trigger_level_up_modal()` (line ~4630)
3. Delete `_project_level_up_ui_from_game_state()`
4. Redirect ~26 `_is_state_flag_true` usages in world_logic.py to rewards_engine
5. Refactor `agents.py` ~110-line function → 3-line delegate to `rewards_engine.is_level_up_active()`
6. Add 4 integration tests from design doc Layer 2
7. Add CI gate for world_logic.py line count upper bound (rev-v4ci04)

## Beads Tracking
- `rev-v4ci01`: Layer 3 CLEAN: strip world_logic.py to ~1500 lines
- `rev-v4ci02`: Layer 3 CLEAN: add design doc Layer 2 integration tests
- `rev-v4ci03`: Layer 3 CLEAN: agents.py _is_character_creation_or_level_up_active → delegate
- `rev-v4ci04`: Layer 3 CLEAN: add CI gate for world_logic.py line count upper bound

## Related PRs
- #6262, #6263, #6264, #6268 — four open PRs superseded by #6276 (attempted partial fixes that duplicated each other)
