---
title: "Phase 2: Consolidate 6 schedule plists into single scheduler daemon"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-1rz8"
priority: P2
issue_type: task
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [task]** Phase 2: Consolidate 6 schedule plists into single scheduler daemon

## Details
- **Bead ID:** `jleechan-1rz8`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

Replace 6 ai.openclaw.schedule.*.plist files with one ai.openclaw.scheduler.plist that reads cron/jobs.json. Also: merge agento 3->1 plist, lifecycle 2->1 plist. Reduces plist count from 25 to ~14. See roadmap/SIMPLIFICATION_PLAN.md.

