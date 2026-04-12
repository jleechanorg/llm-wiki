---
title: "Gemini session format mismatch: .json extension but JSONL reader"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-iv30"
priority: P1
issue_type: bug
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [bug]** Gemini session format mismatch: .json extension but JSONL reader

## Details
- **Bead ID:** `jleechan-iv30`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

agent-gemini/src/index.ts sets sessionFileExtension: '.json' but getActivityState in agent-base calls readLastJsonlEntry(sessionFile) which expects newline-delimited JSON. Gemini writes standard JSON objects. This will cause parse errors or false inactivity detection.

