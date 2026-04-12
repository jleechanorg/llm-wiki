---
title: "Phase 4: Extract shared utility modules (~30 duplicate functions)"
type: source
tags: ["task", "p3", "bead"]
bead_id: "jleechan-81ba"
priority: P3
issue_type: task
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [task]** Phase 4: Extract shared utility modules (~30 duplicate functions)

## Details
- **Bead ID:** `jleechan-81ba`
- **Priority:** P3
- **Type:** task
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

Extract datetime_util.py, path_util.py, slack_util.py, jsonfile_util.py, event_util.py from 12+ orchestration files. Standardize 15 files on gh_integration.gh() instead of raw subprocess.run. See roadmap/SIMPLIFICATION_PLAN.md.

