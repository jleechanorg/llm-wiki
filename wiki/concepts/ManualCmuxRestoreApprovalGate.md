---
title: "Manual cmux restore approval gate"
type: concept
tags: [cmux, authorization, policy, safety]
last_updated: 2026-07-12
---

# Manual cmux restore approval gate

Manual cmux restoration is a current-turn authorization gate. An agent must not manually restore cmux workspaces, surfaces, active session files, or saved coding-agent processes unless the most recent live user message both requests the restore and contains the exact case-sensitive phrase `CMUX RESTORE APPROVED`.

## Why it exists

Manual restore is multiplicative: it can recreate windows, workspaces, surfaces, and agent processes. Treating stale instructions as still active can multiply side effects after the user has already narrowed scope or told the agent to stop.

## Covered actions

- `cmux restore-session`
- socket method `session.restore_previous`
- replacing the active cmux session file for restoration
- reconstructing saved surfaces or sending resume commands that relaunch coding CLIs

## Not covered

- read-only diagnostics
- backup creation
- cmux's normal automatic restoration when the user opens the app

## Operational rule

Check the latest live user message only. Prior turns, summaries, goals, saved prompts, and policy discussion are not authorization. If a newer stop or read-only instruction exists, restore authorization is revoked.

## Sources

- [Manual cmux restore requires explicit approval](../sources/feedback-2026-07-12-manual-cmux-restore-requires-approval.md) — primary source

