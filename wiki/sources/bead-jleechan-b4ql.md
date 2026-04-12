---
title: "Schema real API validation blocked by MCP/API connection refused"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-b4ql"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Schema real API validation blocked by MCP/API connection refused

## Details
- **Bead ID:** `jleechan-b4ql`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

`testing_mcp/schema/test_schema_validation_real_api.py` cannot execute reliably in `--server` mode due connection errors before test execution completes. Reproduced runs show `<urlopen error [Errno 61] Connection refused` when calling MCP tool methods (e.g., `update_user_settings`) after startup logs indicate test-server may be unavailable/unstable.

Evidence: `/tmp/worldarchitectai/schema_followup/schema_validation_real_api/test_console_output.txt` and `/tmp/worldarchitectai/schema_followup/schema_validation_real_api/iteration_004/test_console_output.txt` contain connection refused tracebacks during base_test `_run_single` setup. The command did print server startup and then dropped before processing scenarios.

