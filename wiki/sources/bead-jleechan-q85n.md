---
title: "IMPORTANT: MCP config never updates after initial setup"
type: source
tags: ["task", "p1", "bead"]
bead_id: "jleechan-q85n"
priority: P1
issue_type: task
status: open
created_at: 2026-03-16
updated_at: 2026-03-16
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [task]** IMPORTANT: MCP config never updates after initial setup

## Details
- **Bead ID:** `jleechan-q85n`
- **Priority:** P1
- **Type:** task
- **Status:** open
- **Created:** 2026-03-16
- **Updated:** 2026-03-16
- **Author:** jleechan
- **Source Repo:** .

## Description

setupMcpMailInWorkspace returns early if mcp-agent-mail already exists. Token rotation or URL changes are never propagated. Fix: remove early return or add update logic.

