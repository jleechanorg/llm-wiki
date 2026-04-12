---
title: "Unused writeJsonl helper in cursor activity-detection tests"
type: source
tags: ["task", "p3", "bead"]
bead_id: "jleechan-w6yr"
priority: P3
issue_type: task
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [task]** Unused writeJsonl helper in cursor activity-detection tests

## Details
- **Bead ID:** `jleechan-w6yr`
- **Priority:** P3
- **Type:** task
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

packages/plugins/agent-cursor/src/__tests__/activity-detection.test.ts defines a writeJsonl helper that is never used. Cursor stores sessions in SQLite not JSONL — vestigial from copy-paste from Claude Code tests. Should be removed.

