---
title: "CRITICAL: Bearer token in worktree settings.json"
type: source
tags: ["task", "p0", "bead"]
bead_id: "jleechan-havc"
priority: P0
issue_type: task
status: open
created_at: 2026-03-16
updated_at: 2026-03-16
created_by: jleechan
source_repo: "."
---

## Summary
**[P0] [task]** CRITICAL: Bearer token in worktree settings.json

## Details
- **Bead ID:** `jleechan-havc`
- **Priority:** P0
- **Type:** task
- **Status:** open
- **Created:** 2026-03-16
- **Updated:** 2026-03-16
- **Author:** jleechan
- **Source Repo:** .

## Description

Security issue: MCP_AGENT_MAIL_TOKEN written as Bearer token in settings.json inside worktree. Could be accidentally committed. Fix: pass token via environment variable at runtime instead.

