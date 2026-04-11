---
title: "PR #5715: Fix slash-command PR context detection for fix-comment"
type: source
tags: []
date: 2026-02-26
source_file: raw/prs-worldarchitect-ai/pr-5715.md
sources: []
last_updated: 2026-02-26
---

## Summary
- Fix PR context parsing for slash-command tasks (e.g. `/copilot 5691`) in task dispatcher.
- This prevents fix-comment/fixpr from incorrectly creating new PRs when targeted at an existing PR number.
- Add regression tests for slash command PR detection.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Regex-only change to PR context parsing plus targeted unit tests; minimal blast radius, with the main risk being unintended matching/false positives.
> 
> **Overview**
> Updates `TaskDispa

## Metadata
- **PR**: #5715
- **Merged**: 2026-02-26
- **Author**: jleechan2015
- **Stats**: +39/-0 in 2 files
- **Labels**: none

## Connections
