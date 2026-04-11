---
title: "PR #115: [agento] fix(scm-github): reduce Bugbot severity false positives in merge gate"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-115.md
sources: []
last_updated: 2026-03-23
---

## Summary
The merge gate Bugbot check (condition #4) uses keyword matching to determine comment severity. Words like "bug" and "error" appearing anywhere in cursor[bot] comment bodies caused false positives, mapping review suggestions to severity=error and blocking genuinely green PRs from auto-merge.

## Metadata
- **PR**: #115
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +107/-6 in 2 files
- **Labels**: none

## Connections
