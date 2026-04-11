---
title: "Claude Code Complete System Prompt - Raw Capture"
type: source
tags: [claude-code, system-prompt, anthropic, cli, token-optimization]
source_file: "raw/claude_code_complete_system_prompt.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Raw capture of the Claude Code 1.0.108 system prompt (~7,009 tokens), obtained via HTTP proxy interception of Anthropic API calls on 2025-09-08. Documents the complete instructions given to Claude Code, including tone guidelines, tool usage rules, and proactivity policies.

## Key Claims
- **Concise output requirement**: Responses must be under 4 lines unless user asks for detail; one word answers preferred
- **No unnecessary preamble/postamble**: Avoid "Here is the answer..." style framing
- **Minimal output tokens**: Minimize tokens while maintaining helpfulness
- **Tone guidelines**: Concise, direct, to the point; no emojis unless explicitly requested
- **Proactivity balance**: Allowed when user asks; don't surprise with unsanctioned actions
- **Professional objectivity**: Prioritize technical accuracy over validating user beliefs

## Key Quotes
> "You MUST answer concisely with fewer than 4 lines (not including tool use or code generation), unless user asks for detail."
> "Do not add additional code explanation summary unless requested by the user."
> "Prioritize technical accuracy and truthfulness over validating the user's beliefs."

## Connections
- [[Claude Code Complete System Prompt]] — related capture
- [[Context Components Reference]] — context architecture for token management
- [[CLAUDE.md Compression Analysis]] — token reduction techniques

## Contradictions
- None identified
