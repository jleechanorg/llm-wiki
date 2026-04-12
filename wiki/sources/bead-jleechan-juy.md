---
title: "Create compound CI health agent to prevent fix-chains"
type: source
tags: ["feature", "p1", "bead"]
bead_id: "jleechan-juy"
priority: P1
issue_type: feature
status: open
created_at: 2026-02-19
updated_at: 2026-02-19
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [feature]** Create compound CI health agent to prevent fix-chains

## Details
- **Bead ID:** `jleechan-juy`
- **Priority:** P1
- **Type:** feature
- **Status:** open
- **Created:** 2026-02-19
- **Updated:** 2026-02-19
- **Author:** jleechan2015
- **Source Repo:** .

## Description

CI fix-chains consume human attention: 6 serial CI fix PRs in 3 days (Feb 17-19): #5602 → #5605 → #5620 → #5623 → #5624 → #5634. Each was a reactive fix to the previous. Create a scheduled agent prompt that runs all CI workflows on a test PR, reports all failures, and fixes them in a single compound PR instead of serial one-at-a-time fixes.

