---
title: "Claude Code System Prompt Capture - Method Comparison"
type: source
tags: [claude-code, system-prompt, anthropic, debugging, api, http-proxy]
source_file: "raw/worldarchitect.ai-claude-code-system-prompt-capture-method-comparison.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Tested two working methods for capturing Claude Code's system prompt: Claude CLI debug mode (`claude --debug api`) and HTTP proxy interception. Both successfully captured the complete ~32KB system prompt. A third method (ccproxy-api) failed due to Pydantic compatibility issues.

## Key Claims
- **Debug Method**: Works immediately with `claude --dangerously-skip-permissions -p "test"`, no setup required
- **HTTP Proxy Method**: Clean JSON capture via custom Python proxy server, better for programmatic analysis
- **System Prompt Size**: 32,532 bytes total (~32KB)
- **Content Structure**: Basic identity (58 bytes) + full instructions (~32KB)
- **ccproxy-api Failed**: Pydantic model compatibility issues in version 0.1.7

## Key Quotes
> "Both working methods successfully captured the complete ~32KB system prompt that Claude Code sends to the Anthropic API."

## Connections
- [[ClaudeCode]] — tool being analyzed
- [[Anthropic]] — company providing the API
- [[Pydantic]] — library causing compatibility issues in ccproxy-api

## Contradictions
- []
