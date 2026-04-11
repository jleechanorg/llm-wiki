---
title: "PR #160: feat(lifecycle): emit session.spawned/exited events + fix(tmux): submit queued messages"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-160.md
sources: []
last_updated: 2026-03-24
---

## Summary
Two related changes on `fix/orch-kgn`:

1. **Lifecycle events**: AO workers emit `session.spawned` and `session.exited` events, mapped from `spawning` and `terminated` status transitions in `lifecycle-manager.ts`. These enable the human-channel bridge (jleechanclaw PR #392) to mirror AO worker lifecycle into Slack channel `C0ANK6HFW66`.

2. **Tmux queued messages**: Fix queued tmux messages being incorrectly marked as delivered instead of submitted.

## Metadata
- **PR**: #160
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +64/-44 in 1 files
- **Labels**: none

## Connections
