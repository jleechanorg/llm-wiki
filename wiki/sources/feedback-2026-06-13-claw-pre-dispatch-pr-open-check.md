---
title: "2026-06-13 Claw Pre Dispatch Pr Open Check"
type: source
tags: ["feedback", "worldarchitect"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_claw_pre_dispatch_pr_open_check.md
---

## Summary
Before any /claw \

## Key Claims
- 1. `gh pr view <N> --json state` — must be OPEN
- 2. `gh pr list --state all --search "<scope> in:title"` — check for superseder/successor PRs the user may have created
- 3. If user mentioned "cleaner rebase" / "I closed X" / "rebased" in any recent thread — look for the new PR
- - DO NOT silently re-target to the new PR without confirming with the user. The rebase may have changed scope, removed files, or split the work.
- - Surface: "PR #N was closed at <time>. Closest open PR: #M (<title>). Pivot Hermes to #M, or wait for your call?" Then post the pivot in the existing thread.
- - The dispatch thread is durable; just post a new message with the redirect. Hermes will see it in context and switch.

## Connections
- [[feedback-2026-06-13-claw-slack-dispatch]]
