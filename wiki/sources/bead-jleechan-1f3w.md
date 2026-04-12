---
title: "cursor plugin PR #473: fix misleading session path in PR description (says JSONL, is SQLite)"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-1f3w"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** cursor plugin PR #473: fix misleading session path in PR description (says JSONL, is SQLite)

## Details
- **Bead ID:** `jleechan-1f3w`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

PR #473 description says 'Session path: ~/.cursor/projects/ (JSONL)' but toCursorProjectPath is DEPRECATED and Cursor actually stores sessions in SQLite at ~/.cursor/chats/. Fix before ComposioHQ review.

