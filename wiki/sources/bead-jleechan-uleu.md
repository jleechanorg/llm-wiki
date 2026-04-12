---
title: "task_engine: rename modules to match right-contract spec (config_loader→config, providers→api_client, tools→tool_manager)"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-uleu"
priority: P2
issue_type: task
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [task]** task_engine: rename modules to match right-contract spec (config_loader→config, providers→api_client, tools→tool_manager)

## Details
- **Bead ID:** `jleechan-uleu`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

Right contract required_artifacts specifies config.py, api_client.py, tool_manager.py. Coder delivered config_loader.py, providers.py, tools.py respectively. Either rename files to match spec or update the spec to match delivered names. All imports and tests must stay green after rename.

