---
title: "MODERATE: MCP mail auto-configured without opt-in"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-e5x4"
priority: P2
issue_type: task
status: open
created_at: 2026-03-16
updated_at: 2026-03-16
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [task]** MODERATE: MCP mail auto-configured without opt-in

## Details
- **Bead ID:** `jleechan-e5x4`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-03-16
- **Updated:** 2026-03-16
- **Author:** jleechan
- **Source Repo:** .

## Description

Default MCP mail URL (http://127.0.0.1:8765/mcp/) written to settings even when no server running. No opt-in mechanism. Fix: require explicit env var to enable.

