---
title: "PR #6276"
type: entity
tags: ["pull-request", "rewards-engine", "level-up", "refactor", "world-logic"]
sources: ["pr6276_design_doc_v4_summary"]
last_updated: 2026-04-15
---

## Description
PR #6276 (feat/world-logic-clean-layer3) implements the "Rewards Engine: Single-Responsibility Pipeline Refactor" v4 design. It consolidates all rewards/progression decisions into `rewards_engine.py` and makes `world_logic.py` a thin modal wrapper.

## Status
**OPEN** — ~75% implemented, all CI gates green, Layer 3 CLEAN remaining

## Branch
`feat/world-logic-clean-layer3`

## Key Changes
- `llm_parser.py` (renamed from `streaming_orchestrator.py`) — single orchestration root (1060 lines)
- `rewards_engine.py` — new file with full public API (491 lines)
- `world_logic.py` — reduced from ~9094 to 8729 lines (target ~1500)
- `.github/workflows/design-doc-gate.yml` — new CI grep gate workflow (131 lines)

## CI Status
All 5 grep gates passing:
- ✅ world_logic.py 0 rewards_engine imports
- ✅ constants.py get_xp_for_level/get_level_from_xp deleted
- ✅ _is_state_flag_true in 2 files
- ✅ world_logic.py 0 re.project_level_up_ui calls
- ✅ llm_parser.py canonicalize_rewards=1

## Remaining Work
1. Strip world_logic.py from 8729 to ~1500 lines (rev-v4ci01)
2. Add 4 integration tests from design doc Layer 2 (rev-v4ci02)
3. Refactor agents.py ~110-line function → 3-line delegate (rev-v4ci03)
4. Add CI gate for world_logic.py line count (rev-v4ci04)

## Superseded PRs
This PR supersedes four open PRs that attempted partial fixes: #6262, #6263, #6264, #6268

## Design Doc
`roadmap/level-up-engine-single-responsibility-design-2026-04-14.md`
