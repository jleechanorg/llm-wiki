---
title: "/contexte Command Universal Composition Fix"
type: source
tags: [contexte, universal-composition, claude-code, slash-commands, command-fix]
sources: []
last_updated: 2026-04-07
---

## Summary
Fixed the `/contexte` command which was attempting to use "Universal Composition" to call the built-in `/context` command - an approach that doesn't work because Claude cannot programmatically invoke built-in slash commands from responses. Updated both `/contexte` and `/review-enhanced` to use direct implementation patterns instead.

## Key Claims
- **Built-in Command Limitation**: Claude cannot directly invoke built-in slash commands (like `/context`) from within responses - they require user invocation
- **Universal Composition Scope**: Works only for custom command coordination, not for built-in command invocation
- **Working Pattern**: Direct implementation by Claude rather than trying to orchestrate built-in commands
- **User-Data Driven Approach**: `/contexte` now looks for recent `/context` output in conversation history and analyzes real usage data

## Key Learnings
1. Built-in commands cannot be invoked programmatically by Claude from responses
2. Working commands provide direct analysis rather than trying to orchestrate built-in commands
3. Universal Composition is for custom command coordination, not built-in command access
4. User-driven data approach works better than attempting system integration

## Files Updated
- `~/.claude/commands/contexte.md` - Global command file
- `~/.claude/commands/review-enhanced.md` - Global command file
- `.claude/commands/contexte.md` - Project-specific command file