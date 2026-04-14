# PR #3: feat(agent-cursor): add cursor-agent plugin

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-14
**Author:** jleechan2015
**Stats:** +3864/-0 in 8 files

## Summary
- New agent plugin for Cursor Agent CLI (cursor-agent)
- Based on agent-claude-code template with adaptations for cursor CLI

## Raw Body
## Summary
- New agent plugin for Cursor Agent CLI (cursor-agent)
- Based on agent-claude-code template with adaptations for cursor CLI

## Changes
- Added packages/plugins/agent-cursor/ with package.json, src/index.ts, tsconfig.json

## Key differences from claude-code:
- Binary: cursor-agent (not claude)
- Session storage: ~/.cursor/chats/ (SQLite)
- Resume: --resume [chatId]

## Testing
- Build passes

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Adds a new agent plugin with non-trivial process detection logic (`tmux`/`ps` parsing plus caching) that could affect session liveness reporting; otherwise changes are additive and gated behind using the new plugin.
> 
> **Overview**
> Adds a new `agent-cursor` plugin that can launch `cursor-agent`, set runtime environment (e.g. blank `CLAUDECODE`, `AO_SESSION_ID`), detect activity from terminal output, and determine whether a session is still running via `tmux` pane TTY + cached `ps` scanning or PID checks.
> 
> Cursor session introspection/restore and workspace hooks are explicitly stubbed (returning `null` / no-op) because Cursor stores chats in SQLite, and the PR adds Vitest coverage for command generation, activity classification edge cases, and process detection. Also adds a standalone shell unit test reproducing a tilde-expansion bug in `ao-doctor`, updates `pnpm-lock.yaml`, and introduces a new `package-lock.json`.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 4c9f34790803dd724a0baa17b52abe45703771e5. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Added a new Agent Cursor plugin with launch/restore commands, environment handling, activity classification, session inspection scaffolding, and workspace hook installation
