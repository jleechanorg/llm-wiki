---
title: "PR #203: feat(core): add stuck worker detector for overnight monitoring loops"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-203.md
sources: []
last_updated: 2026-03-26
---

## Summary
Overnight monitoring loops log idle forever because tmux has-session returns ALIVE even when the agent CLI has exited -- the bash shell stays alive in the tmux pane. Workers stuck waiting for user feedback or that have exited without creating PRs are never detected or cleaned up.

## Metadata
- **PR**: #203
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +784/-1 in 4 files
- **Labels**: none

## Connections
