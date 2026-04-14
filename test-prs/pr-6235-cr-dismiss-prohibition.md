---
title: "PR #6235: [agento] fix(harness): add CR dismiss prohibition + refactor evidence rule"
type: test-pr
date: 2026-04-13
pr_number: 6235
files_changed: [CLAUDE.md]
---

## Summary
Post-mortem harness fix for PR #6233 (level/XP centralization), which was merged without CodeRabbit APPROVED review (CR reviews were dismissed, not approved), without evidence bundle (falsely classified as "pure refactor"), and with false 7-green /polish report.

## Key Changes
- **CLAUDE.md**: Added 2 harness rules:
  1. Never dismiss CodeRabbit or Cursor Bugbot CHANGES_REQUESTED reviews - wait for re-review and APPROVED
  2. No refactor evidence exemption - PRs that delete/move/rename production code require evidence bundles

## Motivation
Prevents future regressions by enforcing proper CR review handling and evidence requirements for all production code changes.