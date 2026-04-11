---
title: "Slash Commands Documentation"
type: source
tags: [slash-commands, worldarchitect, claude-code, performance, timeout, cerebras, deployment]
sources: []
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Comprehensive documentation for all slash commands in the WorldArchitect.AI project. Documents performance optimization commands (/timeout), command execution patterns (/execute, /plan, /replicate), and utility commands (/cerebras, /header, /deploy). The system supports universal command composition allowing arbitrary combinations via Claude's NLP.

## Key Claims

- **TIMEOUT Command** — Performance optimization preventing API timeouts: reduces CLI timeout rate from 10% to <2% through tool batching, response limits, thinking constraints, and file operation limits. Three modes: standard, strict, and emergency. Chainable with other commands.

- **Command Execution** — Key commands: /execute (no approval), /plan (requires approval), /replicate (PR analysis). ONE unified /learn command with Memory MCP integration.

- **Universal Composition** — ANY command combination works via Claude's NLP. Commands /think, /learn, /debug, /analyze, /fix, /plan, /execute, /arch, /test, /pr, /perp, /research automatically integrate memory context.

- **/cerebras** — Generates large amounts of code using Cerebras API for 19.6x faster code generation. Best for well-defined code generation tasks, templates, and algorithms. Short aliases: /c, /qwen, /cereb.

- **/header** — Generates mandatory branch header for CLAUDE.md compliance with git status and PR inference. Alias: /usage. Automatically detects branch, upstream, and associated PR.

- **/deploy** — Executes repository's deploy.sh workflow from project root or scripts/ directory. Supports staging and stable targets.

## Connections

- [[WorldArchitect.AI]] — Project containing these slash commands
- [[Claude Code]] — Underlying CLI platform for slash command execution

## Contradictions

- None identified