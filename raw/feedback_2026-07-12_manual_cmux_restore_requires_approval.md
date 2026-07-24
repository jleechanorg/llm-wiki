---
name: Manual cmux restore requires explicit approval
description: Manual cmux restoration is forbidden unless the latest live user message requests it and contains CMUX RESTORE APPROVED.
type: feedback
bead: none
---

# Manual cmux restore authorization gate

## Context

On 2026-07-12, repeated manual cmux restore actions created three near-duplicate windows with 83 workspaces and 95 surfaces. The agent continued treating earlier restore instructions as active after the user told it to stop, then misclassified a short stable snapshot as proof the practical problem was resolved.

## Rule

Do not manually restore cmux workspaces, surfaces, active session files, or saved coding-agent processes unless the most recent live user message both requests the restore and contains the exact case-sensitive phrase `CMUX RESTORE APPROVED`.

The phrase in prior turns, summaries, goals, saved prompts, policy text, or a message that merely discusses the gate is not authorization. A newer stop or read-only instruction always revokes earlier restore intent.

The gate includes:

- `cmux restore-session` and socket method `session.restore_previous`.
- Replacing the active cmux session file for the purpose of restoration.
- Creating/reconstructing saved surfaces or sending manual resume commands to relaunch their coding CLIs.

It does not block read-only diagnostics, backup creation, or cmux's normal automatic restoration when the user opens the app. Keep `terminal.autoResumeAgentSessions=true` unless the user separately asks to change automatic app-start behavior.

## Verification

- User policy updated at `/Users/jleechan/.codex/AGENTS.md` on 2026-07-12.
- `terminal.autoResumeAgentSessions` was restored to `true` and config validation passed.
- No manual restore command was run while recording this learning.

## Reusable pattern

Destructive or multiplicative recovery actions need current-turn authorization. Do not infer authorization from historical context after the user has narrowed scope or said stop.
