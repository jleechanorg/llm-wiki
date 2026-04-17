---
title: "CodeRabbitStaleLineRefs"
type: concept
tags: []
sources: []
last_updated: 2026-04-16
---

## Summary
CodeRabbit inline comments reference specific line numbers from the diff as of when CR first posted. When large refactors land before CR re-reviews, those line refs become stale — pointing to wrong code.

## Pattern
When a PR lands a large refactor (function renames, line deletions, large moves), CR's inline comments still reference the OLD line numbers from the pre-refactor diff. The reported issue may or may not actually exist at those line numbers in the current code.

## Symptoms
- CR posts CHANGES_REQUESTED with line refs like `world_logic.py:1708-1749`
- Actual code at those lines has changed since the comment was posted
- Acting on the line ref without verifying may address non-existent issues

## How to Verify
1. Read the actual current code at the reported line range
2. If the code doesn't match the reported issue → CR is seeing a stale diff
3. Push new substantive changes to trigger re-review, or explicitly dismiss

## Example
PR #6308: CR said `world_logic.py:1708-1749` — `rewards_box` unused and explicit-false guards missing. Actual code at those lines (after 6 prior fix commits):
- `_resolve_level_up_signal()` uses `rewards_box.get("resolved_target_level")` (line 1734)
- Has `_is_state_flag_false` guards (lines 1747-1750)
- CR was reviewing the pre-refactor diff state

## Connections
- [[CodeRabbitDismissedPattern]] — CR DISMISSED also requires understanding diff state
- [[PR6308]] — affected PR
