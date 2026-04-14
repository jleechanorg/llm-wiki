# PR #4: feat(agent-gemini): add gemini-cli plugin

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-14
**Author:** jleechan2015
**Stats:** +1949/-0 in 5 files

## Summary
- New agent plugin for Gemini CLI (gemini)
- Based on agent-claude-code template with adaptations for gemini CLI

## Raw Body
## Summary
- New agent plugin for Gemini CLI (gemini)
- Based on agent-claude-code template with adaptations for gemini CLI

## Changes
- Added packages/plugins/agent-gemini/ with package.json, src/index.ts, tsconfig.json

## Key differences from claude-code:
- Binary: gemini
- Headless mode: -p/--prompt
- Resume: -r/--resume [session]

## Testing
- Build passes

🤖 Generated with Claude Code

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Introduces a new agent plugin that spawns processes, inspects local Gemini session files, and writes workspace hook configuration; incorrect path/process assumptions or hook misconfiguration could impact agent monitoring or developer workspaces.
> 
> **Overview**
> Adds a new `packages/plugins/agent-gemini` workspace package implementing an `Agent` for the Gemini CLI (`gemini`) with launch/restore command generation (including permission/model handling) and environment setup.
> 
> Implements runtime monitoring by detecting the `gemini` process (tmux TTY scan + cached `ps` output or PID checks), classifying activity from terminal output and from the latest Gemini chat JSON files under `~/.gemini/tmp/<sha256(workspace)>/chats`, and extracting session summary/cost from the tail of large session files.
> 
> Adds workspace hook setup that writes a `.gemini/metadata-updater.sh` script and merges `PostToolUse` hooks into `.gemini/settings.json`, plus a comprehensive Vitest suite covering command/env generation, process detection, activity/state inference, and JSON parsing.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 01a9811b6e97067f39e59b12eb98a6cd702edb04. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

* **New Features**
  * Added a Gemini agent plugin delivering launch/configuration, activity
