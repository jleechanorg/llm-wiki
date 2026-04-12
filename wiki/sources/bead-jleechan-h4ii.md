---
title: "Cursor test suite has copy-paste 'Claude Code' labels throughout"
type: source
tags: ["task", "p3", "bead"]
bead_id: "jleechan-h4ii"
priority: P3
issue_type: task
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [task]** Cursor test suite has copy-paste 'Claude Code' labels throughout

## Details
- **Bead ID:** `jleechan-h4ii`
- **Priority:** P3
- **Type:** task
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

Multiple test names and describe blocks in agent-cursor/src/index.test.ts and activity-detection.test.ts say 'Claude Code' or 'claude-code'. Top-level describe in activity-detection.test.ts is named 'Claude Code Activity Detection'. Rename all to reference Cursor.

