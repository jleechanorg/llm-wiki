---
title: "Hook Matcher Tool Agnostic"
type: concept
tags: [hooks, tool-matching, agent-orchestration, gemini, codex]
sources: []
last_updated: 2026-04-11
---

## Description
PostToolUse hooks that are hardcoded to match only "Bash" tool names will miss all other tool invocations (e.g., Gemini's `run_shell_command`, Codex's equivalent). This silently drops metadata updates for non-Bash tool sessions.

## Symptoms
- Metadata not updated when Gemini agent runs commands
- Evidence bundles missing tool call records from Gemini sessions
- PostToolUse hook never fires despite tool invocations occurring

## Root Cause
Hook installer uses hardcoded matcher:
```python
matcher: 'Bash'  # hardcoded — misses Gemini run_shell_command, etc.
```

## Fix
Use a tool-agnostic matcher that fires on any tool invocation:
```python
# Instead of matching 'Bash', match any tool use
matcher: lambda tool_name: tool_name is not None  # any tool
# Or use a whitelist of known shell-like tools
shell_tools = {'Bash', 'run_shell_command', 'shell', 'bash', 'Command'}
matcher: lambda tool_name: tool_name in shell_tools
```

## Connections
- [[AgentAdapter]] — tool adapters normalize tool names across CLIs
- [[PostToolUse]] — metadata update hook system
