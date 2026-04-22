---
title: "ZFC PR Task Specs 2026-04-22"
type: source
tags: [zfc, level-up, roadmap, execution, PR-lanes]
date: 2026-04-21
source_file: /Users/jleechan/roadmap/zfc-pr-task-specs-2026-04-22.md
---

## Summary
Converts the canonical ZFC level-up roadmap into 8 execution-ready task specs for new PR lanes beyond the currently open #6420, #6404, and #6434. Defines ownership model, tracking states, blocker definition, per-item verification methods, and recommended execution order.

## Key Claims
- Roadmap is detailed at stage level but not fully at tracker/per-PR level
- Bead layer was not sufficient before this pass (items 2-8 lacked dedicated branch-ready beads)
- File plus bead updates created on 2026-04-22 close the gap (beads not yet found in local store)
- Date suffix retained because in-flight workers already spawned against exact path

## Current Mapping (Items 1-8)
| Item | Lane | Bead |
|------|------|------|
| 1 | Replacement narrow enforcement PR | rev-lmdo |
| 2 | M1 model compliance MVP evidence PR | rev-23eq |
| 3 | M2 delete project_level_up_ui wrapper | rev-7yt7 |
| 4 | M2 remove resolve_level_up_signal new-path usage | rev-cujw |
| 5 | M2 delete world_logic.py duplicate resolver | rev-usv2 |
| 6 | M2 delete game_state.py duplicate resolver | rev-c726 |
| 7 | M2 remove deprecated prompt/schema aliases | rev-ahpi |
| 8 | M3 final enforcement PR | rev-v0x7 |

## Tracking States
`bead only` → `branch opened` → `draft PR open` → `blocked` → `done`

## Blocker Definition
A lane is blocked when an explicit roadmap prerequisite is missing (not just test failure churn). Worker should report blocker directly and avoid padding branch with speculative work.

## Connections
- [[Level-Up Bug Chain]] — relates to ZFC level-up cleanup chain
- [[Normalization Atomicity]] — canonicalize_rewards single-owner enforcement
- [[Roadmap ZFC Level-Up Model Computes]] — upstream design doc
- [[Roadmap Nextsteps Level-Up ZFC]] — queue context
- [[PR #6420]] — active M0 cleanup lane
- [[PR #6404]] — active architecture lane
- [[PR #6434]] — optional side refactor
