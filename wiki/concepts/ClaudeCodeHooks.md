---
title: "Claude Code Hooks"
type: concept
tags: [claude-code, hooks, configuration]
sources: [tdd-tests-claude-settings-hook-validation]
last_updated: 2026-04-08
---

Hooks in Claude Code are event-based triggers configured in `.claude/settings.json`. They can run on events like PreToolUse, PostToolUse, Stop, and UserPromptSubmit. The hook configuration includes a command and description. Robust hook patterns are required to prevent system lockouts when environment variables like `$ROOT` are undefined.

See also: [[HookRobustnessPatterns]]
