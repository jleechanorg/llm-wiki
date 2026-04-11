---
title: "PR #174: fix(bd-s4t): kill zombie tmux sessions after PR merge/close"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-174.md
sources: []
last_updated: 2026-03-25
---

## Summary
Merged/closed PRs were leaving zombie tmux sessions that accumulated past the 15-session spawn gate, blocking new spawns. The session-reaper skipped terminal-status sessions assuming they were already dead, but the lifecycle-manager only killed sessions on `merged` status — `killed` (closed PRs) was missed, and the reaper had no explicit PR-state check.

## Metadata
- **PR**: #174
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +1044/-232 in 13 files
- **Labels**: none

## Connections
