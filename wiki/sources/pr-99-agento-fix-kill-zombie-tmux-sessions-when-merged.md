---
title: "PR #99: [agento] fix: kill zombie tmux sessions when merged PR transitions to killed (bd-kki)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-99.md
sources: []
last_updated: 2026-03-23
---

## Summary
Merged PR sessions can still remain alive in tmux if lifecycle evaluation hits
runtime/activity killed paths before merged PR state is observed. This race creates
zombie tmux sessions tied to already-merged PRs.

## Metadata
- **PR**: #99
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +295/-6 in 2 files
- **Labels**: none

## Connections
