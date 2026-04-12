---
title: "Remove MCP mail code from upstream Composio PR #486"
type: source
tags: ["task", "p1", "bead"]
bead_id: "jleechan-s9on"
priority: P1
issue_type: task
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [task]** Remove MCP mail code from upstream Composio PR #486

## Details
- **Bead ID:** `jleechan-s9on`
- **Priority:** P1
- **Type:** task
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

PR #486 (jleechanorg -> ComposioHQ) contains setupMcpMailInWorkspace(), MCP mail env var forwarding in getEnvironment(), and hook calls. This is fork-specific infrastructure not appropriate for upstream. Strip before merging. Commits: c88e1532, fd4694b0, 2ade4ba9.

