---
title: "Claude Code System Prompt - Captured via Debug Mode"
type: source
tags: [claude-code, system-prompt, anthropic, debugging, cli, api]
source_file: "raw/worldarchitect.ai-claude-code-system-prompt-captured-via-debug-mode.md"
sources: []
last_updated: 2026-04-07
---

## Summary
This document contains the complete system prompt that Claude Code CLI sends to the Anthropic API, captured via debug mode. The system prompt is extensive (~2.9MB) and includes core identity, behavioral guidelines, tool usage policies, project context, MCP server instructions, and the file permission system.

## Key Claims
- **Capture Method**: Direct Claude CLI inspection using `--dangerously-skip-permissions` flag
- **Version Captured**: Claude Code 1.0.108
- **Capture Date**: 2025-09-08
- **Total Length**: ~2.9MB of structured instructions
- **Dynamic Elements**: Environment variables, project context, permissions
- **Static Elements**: Core behavioral guidelines and tool policies

## Critical Instructions
- **Defensive Security**: Only assists with defensive security tasks
- **File Creation Bias**: Strong preference against creating new files
- **Integration First**: Always attempt to integrate into existing files
- **Context Optimization**: Proactive context management protocols

## Tool Hierarchy
1. Serena MCP - Semantic operations (preferred)
2. Read/Edit Tools - File operations
3. Bash Tools - System operations (restricted)
4. Specialized MCPs - Domain-specific operations

## Key Sections
- **Core Identity**: Claude Code as Anthropic's official CLI tool
- **Behavioral Guidelines**: Tone, style, verbosity requirements
- **Tool Usage Policies**: Security constraints and usage patterns
- **Project Context**: Environment information and workspace setup
- **MCP Server Instructions**: Detailed instructions from connected MCP servers
- **File Permission System**: Comprehensive tool usage permissions

## Connections
- [[ClaudeCode]] — the CLI tool this system prompt belongs to
- [[Anthropic]] — the company that develops Claude Code
