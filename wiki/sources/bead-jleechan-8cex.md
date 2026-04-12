---
title: "Phase 3: Collapse webhook pipeline from 8 files to 3-4"
type: source
tags: ["task", "p3", "bead"]
bead_id: "jleechan-8cex"
priority: P3
issue_type: task
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [task]** Phase 3: Collapse webhook pipeline from 8 files to 3-4

## Details
- **Bead ID:** `jleechan-8cex`
- **Priority:** P3
- **Type:** task
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

Merge webhook_daemon+bridge->webhook.py, escalation_handler+router->escalation.py, shrink webhook_metrics 253->30 LOC, batch GitHub API calls in reconciler (N->5 repo calls). Also fix github-intake.sh/webhook double-dispatch risk. See roadmap/SIMPLIFICATION_PLAN.md.

