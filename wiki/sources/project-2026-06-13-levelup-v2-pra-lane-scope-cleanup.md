---
title: "2026-06-13 Levelup V2 Pra Lane Scope Cleanup"
type: source
tags: ["project", "worldarchitect", "level-up"]
date: 2026-06-13
source_file: raw/project_2026-06-13_levelup_v2_pra_lane_scope_cleanup.md
---

## Summary
Level-up v2 PR-A (#7528) lane-scope cleanup — 4 out-of-lane commits reverted so the diff vs origin/main is exactly the 3 spec-allowed files

## Key Claims
- PR #7528 branch tip `85513958c7` (local; origin tip was `aee517d445` at start of this
- session, 2 unpushed reverts ahead). After I4 closure at `2dc914e2a5`, four commits
- were piled on top outside the §C/§D lane lock (`mvp_site/prompts/**` only):
- | SHA | Subject | Files | Why out-of-lane |
- | `de8e8b811e` | `feat(runners): set TAR_OPTIONS=--no-same-owner to fix rootless Colima extraction EPERM` | self-hosted-oss/{defaults.sh,docker-compose.yml,start-runner.sh} +1 line each | self-hosted-oss/* not in PR-A lane; broader fix lives in PR #7540 (Colima migration, MERGED in origin/main via b881388b4f) |
- | `6c9525c7e8` | `chore(runners): trigger fresh GHA runs after runner labels variable update` | (empty) | Ceremonial; runners infra, not prompts |

## Connections
- [[feedback_2026-06-11_body_edit_triggers_fresh_green_gate]]
- [[feedback_2026-06-13_dark_factory_introduces_scope_drift]]
- [[feedback_2026-06-13_levelup_v2_scope_drift_stop_f]]
- [[project_2026-06-13_levelup_v2_execution_spec_audit]]
- [[project_2026-06-13_levelup_v2_lane_gate_pipeline]]
- [[project_2026-06-13_levelup_v2_pra_fullsheet_i4_closure]]
