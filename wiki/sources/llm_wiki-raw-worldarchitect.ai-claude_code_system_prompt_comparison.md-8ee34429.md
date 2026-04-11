---
title: "Claude Code System Prompt Capture - Method Comparison"
type: source
tags: [claude-code, system-prompt, debugging, proxy, anthropic-api, research]
source_file: "raw/llm_wiki-raw-worldarchitect.ai-claude_code_system_prompt_comparison.md-8ee34429.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Documents successful methods for capturing Claude Code's system prompt sent to the Anthropic API. Two working methods identified: Claude CLI debug mode and HTTP proxy interception. The system prompt is approximately 32KB in size and includes project-specific instructions, MCP server configurations, and tool permissions.

## Key Claims
- **Debug method works**: `claude --debug api` successfully captures the complete ~32KB system prompt without external dependencies
- **HTTP proxy method works**: Custom Python proxy can intercept API requests and extract system prompts in structured JSON format
- **ccproxy-api failed**: Pydantic model compatibility issues in version 0.1.7 prevent usage
- **System prompt contains project context**: Includes instructions from CLAUDE.md, MCP server setups, and environment variables
- **Security considerations**: Both methods expose API keys in outputs requiring careful file handling

## Key Quotes
> "Successfully tested two different methods for capturing Claude Code's system prompt"
> "System prompt appears after tool permission listings"

## Connections
- [[ClaudeCode]] — the CLI tool being analyzed
- [[Anthropic]] — the API provider whose system prompt is being captured

## Contradictions
- None identified

## Method Comparison

### Debug Method (Recommended)
- Command: `claude --debug api --dangerously-skip-permissions -p "test"`
- Pros: No setup required, works immediately, complete capture
- Cons: Mixed output, manual extraction required

### HTTP Proxy Method
- Setup: Python proxy server routing through localhost
- Pros: Clean JSON format, programmatic processing
- Cons: Setup required, network dependency

### ccproxy-api (Failed)
- Status: Pydantic configuration errors, not usable