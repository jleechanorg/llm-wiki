---
title: "CodeRabbitDismissedPattern"
type: concept
tags: []
sources: []
last_updated: 2026-04-16
---

## Summary
CR DISMISSED means CodeRabbit ran but found nothing to comment on, so it auto-dismisses its review. An empty commit does NOT re-trigger CR re-review. A **substantive code change** is required to get CR to post a new review.

## Pattern
- **CHANGES_REQUESTED**: CR found issues → push fixes → CR re-reviews → may move to COMMENTED or APPROVED
- **DISMISSED**: CR ran but found nothing → auto-dismissed → push of any kind does NOT trigger re-review
- **Workaround for DISMISSED**: Push a **substantive code change** (not empty commit). CR re-triggers on actual diff changes.

## Examples
- PR #6287: CR posted 5 DISMISSED reviews. Pushed empty commit `008c674289` to trigger re-review — CR did NOT re-review. Then pushed substantive fix `5c1875808d` (using `rewards_box` param in `_infer_level_up_target_from_xp`) — CR re-triggered.

## How to Apply
When CR shows DISMISSED on a PR that needs APPROVED (7-green requirement):
1. Do NOT push empty commit to "trigger CI/CR" — it won't work
2. Instead, make a substantive code fix and push that
3. If no real code change is possible, close the PR and re-create with a different approach
