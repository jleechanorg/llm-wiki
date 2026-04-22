---
title: "PR #6370 Review: ASI and XP Display Scope Drift"
type: source
tags: []
date: 2026-04-19
source_file: pr6370_review_comment.md
---

## Summary
A code review of PR #6370 (level-up centralization contract) identified two behavioral changes that go beyond the PR's stated goal of fixing stale level-up flags: (1) ASI choices now apply to single-class characters (previously multiclass-only), and (2) XP display now uses `rewards_pending.xp_gained` instead of computed overflow XP. Both are meaningful behavior changes requiring separate evidence or explicit PR body acknowledgment.

## Key Claims
- ASI choices at levels 4, 8, 12, 14, 16, 19 now fire for single-class characters — previously only multiclass characters triggered this path
- `xp_gained` in rewards_box now reflects `rewards_pending.xp_gained` (e.g., 300) instead of XP above level floor (e.g., 0 for a fresh level-1 character)
- These changes are UI-visible but not disclosed in the PR body, which states "UI evidence is N/A - no UI changes"

## Key Quotes
> "Single-class characters now receive ASI choices at levels 4, 8, 12, 14, 16, 19 — behavior that previously only fired for multiclass characters. This is a meaningful behavior change, not a bug fix."

> "The PR body states 'UI evidence is N/A - no UI changes.' The XP display change is UI-visible."

## Connections
- [[PR 6370]] — the PR under review
- [[Level-Up Centralization Contract]] — the design principle this PR claims to implement
- [[Rewards Engine Architecture]] — where `ensure_rewards_box` lives
