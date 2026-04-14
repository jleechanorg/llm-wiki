# PR #9: refactor(agent-cursor): centralize shared code in agent-base plugin

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-15
**Author:** jleechan2015
**Stats:** +1564/-1494 in 10 files

## Summary
(none)

## Raw Body
Adds @composio/ao-plugin-agent-base and refactors agent-cursor and agent-claude-code as thin wrappers. Rebased cleanly onto main (original plugin was already merged as PR #3).

- Cursor config: --force, no systemPromptFlag, interactive mode via sendMessage
- getRestoreCommand returns null pending SQLite introspection
- 110/110 tests pass
- Design doc: docs/design/agent-cursor-plugin.html

Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Moderate risk because agent lifecycle/introspection logic (launch flags, process detection, JSONL parsing, and workspace hook writing) is centralized and now shared by both `agent-claude-code` and `agent-cursor`, which could change runtime behavior across agents.
> 
> **Overview**
> Introduces new `@composio/ao-plugin-agent-base`, a shared factory (`createAgentPlugin`) that implements the common JSONL-backed `Agent` behaviors: launch command construction (permissionless + model + optional system prompt), process detection with a cached `ps` scan, JSONL tail parsing for `getSessionInfo` (summary + token/cost estimation), activity polling via `readLastJsonlEntry`, and workspace hook installation via a shared `metadata-updater.sh`.
> 
> Refactors both `agent-claude-code` and `agent-cursor` into thin config wrappers around this base. Cursor is switched from “no introspection” to using `~/.cursor/projects/` JSONL for `getSessionInfo`/activity, while explicitly overriding `getRestoreCommand` to `null` (SQLite resume remains unimplemented) and enabling the same workspace hook installation under `.cursor/`.
> 
> Adds a design reference doc (`docs/design/agent-cursor-plugin.html`), updates dependencies/lockfile to include the new base plugin, and fixes Cursor package metadata URLs.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit bd04870622e728e015e7fea256ceb76732a9def3. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab
