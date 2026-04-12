---
title: "repair prompts lack context: CI failure messages are static config strings"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-ylqd"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** repair prompts lack context: CI failure messages are static config strings

## Details
- **Bead ID:** `jleechan-ylqd`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

The send-to-agent reaction in lifecycle-manager.ts:426 sends reactionConfig.message verbatim—a plain static string like 'Fix CI'. No parsed failure details, diff, log excerpts, or failing check names are injected. Agents must independently query gh pr checks. Add context injection: failing check names, summary log tail, and relevant file hints.

