---
title: "dark-factory: claudew deleted, agy reviewer gate + claude fallback"
type: source
tags: [dark-factory, claudew, wafer, agy, reviewer-gate, model-routing]
date: 2026-06-08
source_file: raw/project_2026-06-08_claudew_delete_agy_reviewer_gate.md
---

## Summary
2026-06-08 dark-factory changes (uncommitted on main, alongside unrelated WIP): (1) deleted claudew (wafer/GLM-5.1) backend — removed from handlers.py and __main__.py --backend choices (now echo,claude,codex,ao,agy); (2) added agy reviewer gate with claude infra-failure fallback via _execute_gate helper (real agy fail/partial is kept, never reviewer-shopped); (3) fixed pipelines/slim/review_pr.dot evidence node (was codergen wearing reviewer label, converted to gate_er with explicit backend=agy). Tests 13/13 green; full pytest polluted by 4 untracked WIP test files (lesson: git status first on noisy full-suite failures).

## Key Claims
- claudew backend completely removed — grep for claudew|wafer|glm-5|localhost:9001 in runner/ and pipelines/ is clean
- _resolve_gate_backend needed because engine._run_with_retries calls gates with run-level ctx, so gates historically read ctx.backend not per-node attr — a stylesheet backend=agy on a gate node was silently ignored
- Real agy fail/partial is kept; only infra failures (sandbox unavailable/timed_out/backend_missing) trigger claude fallback with fallback_used=true,fallback_from=agy
- review_pr.dot evidence node was type=codergen (a worker wearing reviewer label — editable, no SHA binding, no verdict parse); converted to type=gate_er with explicit backend=agy
- Full pytest showed 11 failures (4 untracked WIP test files polluted global handler/registry state); tracked-only = 229 passed, 1 failed (pre-existing conformance unrelated)

## Connections
- [[holdout_eval-emulator-infra]]
- [[DarkFactory]]
- [[ModelStylesheet]]
- [[AgyReviewerGate]]
