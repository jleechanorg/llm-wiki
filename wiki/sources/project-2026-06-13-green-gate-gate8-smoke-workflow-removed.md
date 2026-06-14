---
title: "2026-06-13 Green Gate Gate8 Smoke Workflow Removed"
type: source
tags: ["project", "worldarchitect"]
date: 2026-06-13
source_file: raw/project_2026-06-13_green_gate_gate8_smoke_workflow_removed.md
---

## Summary
mcp-smoke-tests.yml removed in

## Key Claims
- if echo "$CHANGED" | grep -qE '^mvp_site/prompts/|^mvp_site/.+\.py$'; then
- - `mvp_site/prompts/...` (prompts)
- - `mvp_site/**/*.py` — including `mvp_site/tests/test_*.py`, `mvp_site/world_logic.py`, `mvp_site/llm_service.py`, `mvp_site/llm_providers/*.py`, etc.
- So **every** production PR that touches a `.py` file under `mvp_site/` is deadlocked.
- - [#7518](https://github.com/jleechanorg/worldarchitect.ai/pull/7518) (ratchet, test-only at mvp_site/tests/test_output_token_budget_regression.py)
- - [#7480](https://github.com/jleechanorg/worldarchitect.ai/pull/7480) (no-second-llm, 197+/-1453 across world_logic.py + llm_service.py + provider_utils.py)

## Connections
- [[project-2026-06-13_bq_logging_3pr_closeout]]
