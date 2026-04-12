---
title: "cursor plugin: remove dead METADATA_UPDATER_SCRIPT (setupHookInWorkspace is no-op)"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-mk7z"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** cursor plugin: remove dead METADATA_UPDATER_SCRIPT (setupHookInWorkspace is no-op)

## Details
- **Bead ID:** `jleechan-mk7z`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

agent-cursor/src/index.ts defines ~140 lines of METADATA_UPDATER_SCRIPT (lines 47-183) that is never used. setupHookInWorkspace() is explicitly a no-op because Cursor Agent CLI does not support PostToolUse hooks. Remove the dead script constant.

