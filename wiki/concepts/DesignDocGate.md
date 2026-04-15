---
title: "Design Doc Grep Gate"
type: concept
tags: [ci, design-doc, automation, merge-gate, quality]
sources: [".github/workflows/design-doc-gate.yml"]
last_updated: 2026-04-15
---

## Definition
`design-doc-gate.yml` is a 131-line GitHub Actions CI workflow that enforces design doc grep gates on PRs touching production code. It blocks merge by requiring explicit human approval override when gates FAIL.

## How It Works
The workflow extracts gate commands from design docs in the branch and runs them against the PR head SHA. Gate commands use `check_gate()` bash function that compares expected vs actual values.

## Gates Enforced (Level-Up v4)
| Gate | Expected | Actual | Purpose |
|------|----------|--------|---------|
| world_logic 0 rewards_engine public API imports | 0 | 0 | world_logic is thin consumer |
| world_logic 0 resolve_level_up_signal calls | 0 | 0 | no direct rewards_engine calls |
| constants get_xp_for_level | 0 | 0 | deduped to game_state |
| constants get_level_from_xp | 0 | 0 | deduped to game_state |
| _is_state_flag_true 2 files | 2 | 2 | canonical + class-body exception |
| world_logic 0 re.project_level_up_ui calls | 0 | 0 | no direct calls |
| llm_parser canonicalize_rewards=1 | 1 | 1 | single call site |

## CI Gate Gap
**Problem**: All 5 gates pass but Layer 3 CLEAN work remains incomplete. The workflow tracks structural gates (import counts, file counts, single-call-site) but NOT:
- `world_logic.py` line count upper bound (currently 8729, target ~1500)
- Function deletions (`_maybe_trigger_level_up_modal`, `_project_level_up_ui_from_game_state`)
- `_is_state_flag_true` usage count in `world_logic.py` (~26 non-comment usages)

## Related Beads
- `rev-v4ci04`: Add CI gate for world_logic.py line count upper bound

## Files
- `.github/workflows/design-doc-gate.yml` — the CI workflow
- `roadmap/level-up-engine-single-responsibility-design-2026-04-14.md` — design doc with grep gates section
