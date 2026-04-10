---
title: "Tool Permissions"
type: concept
tags: [security, permissions, claude-code, file-system]
sources: [claude-code-system-prompt-captured-via-debug-mode]
last_updated: 2026-04-07
---

Tool Permissions is Claude Code's security system that controls which commands and tools can be executed. The system prompt includes a comprehensive JSON-based permission structure that defines allowed operations (e.g., `"Bash(git:*)"`, `"Bash(gh:*)"`) with granular control over file system access, shell commands, and tool invocations.

## Permission Examples
- `"Bash(git:*)"` — full git operations
- `"Bash(gh:*)"` — GitHub CLI operations
- File permissions with specific path restrictions

## Security Model
- Defensive security only (no malicious code assistance)
- Restricted Bash tool usage
- Scoped file system access
- MCP server capability filtering
