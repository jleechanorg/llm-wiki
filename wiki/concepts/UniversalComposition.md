---
title: "Universal Composition"
type: concept
tags: [slash-commands, command-coordination, architecture]
sources: [contexte-command-universal-composition-fix]
last_updated: 2026-04-08
---
## Definition
A command coordination pattern that allows custom slash commands to work together. Intended to enable custom commands to orchestrate built-in commands, but was discovered to be limited to custom command coordination only.

## Key Limitation
Universal Composition works for calling other custom commands that delegate to subagents, but cannot invoke built-in CLI slash commands like `/context` or `/review`. Built-in commands require direct user invocation.

## Use Cases
- Custom-to-custom command coordination
- Chaining related custom commands
## Misconception
Was thought to enable built-in command invocation but this never worked in practice.
