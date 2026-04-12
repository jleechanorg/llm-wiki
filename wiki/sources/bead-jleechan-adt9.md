---
title: "task_engine: add test_tool_manager.py — ToolAccessError when agent uses restricted tool"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-adt9"
priority: P2
issue_type: task
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [task]** task_engine: add test_tool_manager.py — ToolAccessError when agent uses restricted tool

## Details
- **Bead ID:** `jleechan-adt9`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

Left contract acceptance test 7 requires test_tool_manager.py covering: Agent with tools=['Read'] raises ToolAccessError when attempting Edit. File was not created by coder — only test_circuit_breaker, test_config_loader, test_engine_integration, test_parallel_executor exist.

