---
title: "Slash Commands"
type: concept
tags: [claude-code, commands, interface, workflow-automation]
sources: []
last_updated: 2026-04-07
---

## Definition
Slash commands are Claude Code's built-in command interface that allows users to invoke predefined workflows, agents, and utilities. Commands are typed in the format `/commandname` in the input box.

## Key Characteristics
- **Prefix**: All commands use `/` as prefix
- **builtins**: Core commands like /copilot, /claw, /e, /status
- **Skills**: User-defined skills invoked via slash commands
- **Agents**: Agent dispatch commands like /research, /agentor, /team-claude

## Usage Patterns (from [[CommandUsageLast30Days]])
- Top 10 commands capture 82% of all invocations
- 69% of tracked commands have zero usage
- /copilot alone accounts for 29% of all command invocations
- "Long-tail" problem: many niche commands rarely used

## Related Concepts
- [[CommandOutputTrimmerHook]] — handles output from slash commands
- [[UserPreferencesPatterns]] — workflow preferences reflected in command choices
- [[HookRefireShortcircuit]] — hooks that modify command behavior
