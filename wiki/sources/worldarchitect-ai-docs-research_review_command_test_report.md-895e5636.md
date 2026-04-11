---
title: "Research Test Report: Default /review Command in Claude Code CLI"
type: source
tags: [claude-code, slash-commands, research, code-review]
sources: []
date: 2025-08-09
source_file: raw/worldarchitect.ai-docs-research_review_command_test_report.md
last_updated: 2026-04-07
---

## Summary
Research on the default `/review` command in Claude Code CLI confirms it is a built-in slash command designed to "Request code review." The command is classified as an interactive mode command that can be customized at the project level with custom implementations in `.claude/commands/review.md`. Projects commonly override the default with enhanced features including GitHub API integration for posting review comments.

## Key Claims
- **Built-in Slash Command**: `/review` is officially a built-in slash command in Claude Code CLI per official Anthropic documentation
- **Default Purpose**: Stated purpose is "Request code review" — provides AI-powered code review analysis
- **Project Customization**: Projects can override with custom implementations in `.claude/commands/review.md` that take precedence over built-in commands
- **Custom Implementation Features**: Enhanced versions include PR detection, GitHub API integration, file-by-file analysis, and categorized issue reporting (Critical, Important, Suggestion, Nitpick)
- **Command Classification**: Interactive mode command (used within Claude Code sessions), not a CLI command

## Key Quotes
> "/review is listed as a built-in slash command" — Official Anthropic documentation

> "The default /review command provides code review functionality" — Official docs state "Request code review"

## Connections
- [[ClaudeCodeCLI]] — the CLI where `/review` is a built-in slash command
- [[SlashCommands]] — category of interactive commands in Claude Code

## Contradictions
- None identified — this is new research content not conflicting with existing wiki knowledge