---
title: "PR #123: [agento] bd-jo6: tmux orphan session TTL/sweep in lifecycle-manager"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-123.md
sources: []
last_updated: 2026-03-24
---

## Summary
The lifecycle-manager runs a polling loop every 30s, but tmux sessions can be orphaned when:
- A lifecycle-manager restart occurs mid-session
- A session is killed outside AO's control
- Metadata files are corrupted or deleted
- Sessions from other AO installations on the same machine accumulate

Over time, these orphans accumulate in tmux and can eventually block the spawn gate (>15 sessions threshold), preventing new PR workers from spawning.

## Metadata
- **PR**: #123
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +818/-5 in 5 files
- **Labels**: none

## Connections
