---
title: "IMPORTANT: Hook matcher hardcoded to Bash"
type: source
tags: ["task", "p1", "bead"]
bead_id: "jleechan-w1k7"
priority: P1
issue_type: task
status: open
created_at: 2026-03-16
updated_at: 2026-03-16
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [task]** IMPORTANT: Hook matcher hardcoded to Bash

## Details
- **Bead ID:** `jleechan-w1k7`
- **Priority:** P1
- **Type:** task
- **Status:** open
- **Created:** 2026-03-16
- **Updated:** 2026-03-16
- **Author:** jleechan
- **Source Repo:** .

## Description

Hook installer uses matcher: 'Bash' hardcoded, so Gemini's run_shell_command won't trigger PostToolUse hook. Metadata won't update for Gemini sessions.

