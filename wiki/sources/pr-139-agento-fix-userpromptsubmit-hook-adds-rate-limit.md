---
title: "PR #139: [agento] fix: UserPromptSubmit hook adds rate-limit guard to PR green-check"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-139.md
sources: []
last_updated: 2026-03-24
---

## Summary
The `UserPromptSubmit` hook fires the PR green-check reminder on every idle prompt, even when:
1. The PR is already MERGED/CLOSED
2. CR review state hasn't changed since the last check
3. A known blocker (e.g. CR rate-limited) is pending

This burns GitHub API rate-limit budget with no actionable outcome.

## Metadata
- **PR**: #139
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +226/-0 in 2 files
- **Labels**: none

## Connections
