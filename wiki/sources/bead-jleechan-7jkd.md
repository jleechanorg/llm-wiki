---
title: "Cursor cost test expects Claude Code pricing (wrong rates)"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-7jkd"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** Cursor cost test expects Claude Code pricing (wrong rates)

## Details
- **Bead ID:** `jleechan-7jkd`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

agent-cursor/src/index.test.ts expects estimatedCostUsd ~0.021 computed from Claude Code's $3/M input, $15/M output rates. But cursorConfig has no defaultCostRate. Test will fail or produce misleading results. Either set a Cursor-specific cost rate or fix the test expectations.

