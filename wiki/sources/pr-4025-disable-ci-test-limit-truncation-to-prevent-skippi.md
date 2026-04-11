---
title: "PR #4025: Disable CI_TEST_LIMIT truncation to prevent skipping critical tests"
type: source
tags: []
date: 2026-01-25
source_file: raw/prs-worldarchitect-ai/pr-4025.md
sources: []
last_updated: 2026-01-25
---

## Summary
Removes the `CI_TEST_LIMIT` test truncation logic that was arbitrarily limiting discovered tests during CI runs. This change ensures all critical tests are executed instead of being skipped due to performance constraints.

## Metadata
- **PR**: #4025
- **Merged**: 2026-01-25
- **Author**: jleechan2015
- **Stats**: +96/-4909 in 11 files
- **Labels**: none

## Connections
