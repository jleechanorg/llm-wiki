---
title: "PR #163: [agento] feat(harness): add auto-merge wait and --auto flag (bd-5gl)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-163.md
sources: []
last_updated: 2026-03-24
---

## Summary
Workers post green signal (6/6 criteria met) but PRs stall permanently — the lifecycle-manager fires the `approved-and-green` reaction and calls `scm.mergePR()`, but the merge gate fails because CI is still completing when the PR transitions to mergeable. The `ao-pr-poller` removal in PR #352 left no replacement for the merge step.

Fix: workers should run `gh pr merge --auto` after green signal + 5min wait.

## Metadata
- **PR**: #163
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +139/-24 in 6 files
- **Labels**: none

## Connections
