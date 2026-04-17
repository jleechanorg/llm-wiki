---
title: "PR #6276 design-doc-gate Failure"
type: source
tags: [worldarchitect.ai, level-up, design-doc, gate-fragmentation, ci/cd, skeptic-agent]
date: 2026-04-15
source_file: null
---

## Summary
PR #6276 (`feat(world_logic): Layer 3 CLEAN`) merged with design-doc-gate FAILING — the `world_logic 0 re.project_level_up_ui calls` grep gate showed 6 actual calls vs 0 expected, but the PR was not blocked. Root cause: three separate gate workflows (green-gate, design-doc-gate, skeptic-gate) with no unified pass/fail signal. The skeptic agent (`ao skeptic verify`) does NOT verify design doc grep gates.

## Key Claims
- design-doc-gate.yml is a separate parallel workflow that FAILs without blocking green-gate
- The skeptic agent (`ao skeptic verify`) evaluates code quality vs PR description but does NOT run design doc grep gates
- PR #6276 had 3984 additions, 1928 deletions across 37 files; world_logic.py is still 8896 lines (target ~1500)
- 2 backward-compat stubs (`_maybe_trigger_level_up_modal`, `_project_level_up_ui_from_game_state`) remain in world_logic.py
- 27 `_is_state_flag_true` call sites still present; 4 integration tests missing; CI line-count gate not implemented

## Connections
- [[level-up-v4-design]] — PR #6276 implements Layer 3 CLEAN from v4 design
- [[skeptic-gate-workflow]] — skeptic workflow does NOT verify grep gates
- [[design-doc-as-contract-skill]] — skill exists but was not invoked for PR #6276
- [[green-gate-workflow]] — green-gate (7-green) does not include design-doc-gate as blocking step
- [[world-logic-layer3-clean]] — remaining scope: 7400 lines to strip, stubs to delete, refs to redirect
