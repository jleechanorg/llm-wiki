---
title: "Research Test Report: Default /review Command in Claude Code CLI"
type: source
tags: [claude-code, slash-commands, research, review-command]
sources: []
last_updated: 2026-04-07
---

## Summary
Research report confirming `/review` is a built-in slash command in Claude Code CLI designed to "Request code review." The command can be customized at the project level via `.claude/commands/review.md`, with custom implementations taking precedence over the built-in default.

## Key Claims
- `/review` is officially a **built-in slash command** in Claude Code CLI according to official Anthropic documentation
- Default behavior provides AI-powered code review analysis with automated feedback on bugs, improvements, and style guide adherence
- Projects can override the default with custom implementations in `.claude/commands/review.md`
- Custom implementations take precedence over built-in commands
- Distinction between built-in and custom shown in `/help` with "(project)" or "(user)" tags
- The command operates in interactive mode within Claude Code sessions, not as a CLI command

## Key Quotes
> "/review is listed as a built-in slash command with the following specification: Command: /review, Purpose: Request code review"
> "Projects can override this with custom implementations in .claude/commands/review.md. Custom implementations take precedence over built-in commands"

## Connections
- [[Claude Code]] — the CLI where `/review` is implemented
- [[Slash Commands]] — category of commands in Claude Code

## Contradictions
- None identified — aligns with existing wiki content confirming `/review` as built-in command