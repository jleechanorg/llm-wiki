---
title: "auto-merge stub: lifecycle never calls scm.mergePR()"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-514o"
priority: P1
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [bug]** auto-merge stub: lifecycle never calls scm.mergePR()

## Details
- **Bead ID:** `jleechan-514o`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

The auto-merge case in executeReaction() (lifecycle-manager.ts:467) just notifies humans via notifyHuman(). scm.mergePR() at line 631 of scm-github/src/index.ts is fully implemented but never called. Wire the lifecycle auto-merge action to call scm.mergePR() to complete the closed-loop autonomy goal.

