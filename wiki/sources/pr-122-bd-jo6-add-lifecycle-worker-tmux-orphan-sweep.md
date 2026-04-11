---
title: "PR #122: bd-jo6: add lifecycle-worker tmux orphan sweep"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-122.md
sources: []
last_updated: 2026-03-23
---

## Summary
The lifecycle-worker currently polls session state but does not proactively reconcile orphan tmux runtime sessions that no longer have AO DB records. Over time, these stale tmux sessions accumulate and can interfere with spawn gating and operational hygiene.

## Metadata
- **PR**: #122
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +276/-118 in 1 files
- **Labels**: none

## Connections
