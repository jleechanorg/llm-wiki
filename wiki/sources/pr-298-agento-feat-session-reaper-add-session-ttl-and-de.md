---
title: "PR #298: [agento] feat(session-reaper): add session TTL and dead-tmux reaping (orch-ju1)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-298.md
sources: []
last_updated: 2026-03-30
---

## Summary
- Add sessionTtlMs config (default 4h) to kill sessions alive longer than configured TTL
- Add dead-tmux detection: tmux has-session failure triggers kill + optional respawn
- Dead tmux + open PR: respawn replacement worker targeting same PR number
- Dead tmux + merged/closed PR: clean up via sessionManager.kill (worktree cleanup)
- Sessions within startup grace period (120s default) are immune to TTL/dead-tmux killing
- 14 new tests covering TTL, dead-tmux, respawn, grace period, and error hand

## Metadata
- **PR**: #298
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +589/-1 in 4 files
- **Labels**: none

## Connections
