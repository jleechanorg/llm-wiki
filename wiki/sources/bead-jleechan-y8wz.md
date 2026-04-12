---
title: "toAgentProjectPath re-exported from Gemini plugin with @deprecated tag but never removed"
type: source
tags: ["task", "p3", "bead"]
bead_id: "jleechan-y8wz"
priority: P3
issue_type: task
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [task]** toAgentProjectPath re-exported from Gemini plugin with @deprecated tag but never removed

## Details
- **Bead ID:** `jleechan-y8wz`
- **Priority:** P3
- **Type:** task
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

packages/plugins/agent-gemini/src/index.ts imports toAgentProjectPath from agent-base and re-exports it @deprecated. Gemini uses toGeminiProjectPath (SHA-256) instead. Dead export should be removed.

