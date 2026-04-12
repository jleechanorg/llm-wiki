---
title: "merge_conflicts status missing from PR_TRACKING_STATUSES"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-n6b9"
priority: P1
issue_type: bug
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [bug]** merge_conflicts status missing from PR_TRACKING_STATUSES

## Details
- **Bead ID:** `jleechan-n6b9`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

New merge_conflicts value was added to SessionStatus and SESSION_STATUS in core/src/types.ts (PR #486) but is not present in PR_TRACKING_STATUSES. claimPR uses this set to determine if a PR can be claimed. Sessions in merge_conflicts state may be incorrectly claimable or invisible to the tracking system.

