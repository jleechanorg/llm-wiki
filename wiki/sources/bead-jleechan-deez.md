---
title: "Gemini hookToolMatcher missing: hooks silently never fire"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-deez"
priority: P1
issue_type: bug
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [bug]** Gemini hookToolMatcher missing: hooks silently never fire

## Details
- **Bead ID:** `jleechan-deez`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

geminiConfig in agent-gemini/src/index.ts omits hookToolMatcher, so it inherits the default 'Bash' matcher. But Gemini uses run_shell_command as its tool name. Result: PostToolUse hooks configured by setupHookInWorkspace never trigger for Gemini agents. Fix: set hookToolMatcher: 'run_shell_command' in geminiConfig.

