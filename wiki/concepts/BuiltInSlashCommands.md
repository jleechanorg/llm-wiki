---
title: "Built-in Slash Commands"
type: concept
tags: [slash-commands, cli, invocation]
sources: [contexte-command-universal-composition-fix]
last_updated: 2026-04-08
---
## Definition
Slash commands bundled with Claude Code CLI that handle common workflows (like `/context`, `/review`, `/learn`).

## Key Property
These commands cannot be invoked programmatically by Claude from within agent responses. They require explicit user invocation.

## Examples
- `/context` — context analysis
- `/review` — code review
- `/learn` — learning extraction
- `/contexte` — now delegates to user-data approach

## Workaround
Instead of programmatic invocation, Claude can prompt users to run these commands and then analyze their output from conversation history.
