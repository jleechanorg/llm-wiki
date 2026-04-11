---
title: "PR #313: fix(poller): repair zombie worktree cleanup, reap ao-* zombies, delete 3 dead modules"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-313.md
sources: []
last_updated: 2026-03-21
---

## Summary
The AO PR poller (`ao-pr-poller.sh`) was silently failing to clean up stray worktrees at `/private/tmp/` paths every cycle. This caused `ao spawn` to fail with `fatal: already checked out` for PRs #311 and #310, leaving those PRs stuck indefinitely with no agent working on them.

Root cause analysis: `cleanup_zombie_worktree` had two bugs, identified via 5 Whys harness analysis in the `jleechanclaw` main session.

Beads: orch-tzc (cleanup bug), orch-gws (ao-* zombies), orch-i61 (test), orch-9yi

## Metadata
- **PR**: #313
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +96/-16 in 3 files
- **Labels**: none

## Connections
