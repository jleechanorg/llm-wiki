---
title: "PR #288: [agento] feat: add productivity-based stall detection to lifecycle-worker"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-288.md
sources: []
last_updated: 2026-03-29
---

## Summary
Lifecycle-worker only checked tmux session liveness, not whether workers were making progress. Workers that exhaust context, stall waiting for CR reviews, or have merged PRs sat idle indefinitely.

## Metadata
- **PR**: #288
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +2304/-86 in 12 files
- **Labels**: none

## Connections
