---
title: "Python Runtime"
type: concept
tags: [python, runtime, architecture, limitations]
sources: []
last_updated: 2026-04-08
---

## Summary
The Python runtime environment where application code executes. It cannot access MCP tools that exist only in Claude Code's execution context.

## Key Details
- Python code runs in the application's runtime environment
- MCP tools are only available to the Claude AI, not to Python
- Architectural separation prevents direct MCP tool invocation from Python
- Workaround: delegate MCP operations to Claude via prompts

## Related Concepts
- [[MCP]] — tools Python cannot access
- [[Memory MCP Integration - Architectural Limitation]] — documents this limitation
