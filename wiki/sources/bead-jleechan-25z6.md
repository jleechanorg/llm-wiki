---
title: "pairv2 verifier must audit right-contract artifact names, not just pytest exit code"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-25z6"
priority: P1
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [bug]** pairv2 verifier must audit right-contract artifact names, not just pytest exit code

## Details
- **Bead ID:** `jleechan-25z6`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The pairv2 verifier currently only checks `pytest` exit code and declares RIGHT_CONTRACT: satisfied. It does not compare delivered file names against `required_artifacts` in the right contract JSON. Result: task_engine delivered config_loader.py/providers.py/tools.py but the contract required config.py/api_client.py/tool_manager.py — verifier said PASS anyway.

