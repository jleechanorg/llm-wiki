---
title: "lifecycle-worker: auto-kill tmux session after PR merged/closed"
type: source
tags: ["bug", "p0", "bead"]
bead_id: "jleechan-v7oa"
priority: P0
issue_type: bug
status: open
created_at: 2026-03-23
updated_at: 2026-03-23
created_by: jleechan
source_repo: "."
---

## Summary
**[P0] [bug]** lifecycle-worker: auto-kill tmux session after PR merged/closed

## Details
- **Bead ID:** `jleechan-v7oa`
- **Priority:** P0
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-23
- **Updated:** 2026-03-23
- **Author:** jleechan
- **Source Repo:** .

## Description

Lifecycle manager detects merged/killed status but never calls sm.kill() to terminate the tmux session. Sessions accumulate indefinitely.

Root cause: lifecycle-manager.ts status transition to 'merged'/'killed' only updates metadata and clears reaction trackers — no call to sm.kill() to terminate the runtime.

Evidence: 10 worker tmux sessions alive right now, all showing Claude waiting for input ('bypass permissions on') after PR work completed.

Fix: After transitioning session to merged/killed, call sm.kill(session.id) to terminate the tmux session.

Manual workaround: ao session cleanup

