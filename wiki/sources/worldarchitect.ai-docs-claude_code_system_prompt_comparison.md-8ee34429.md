---
title: "Claude Code System Prompt Capture - Method Comparison"
type: source
tags: [claude-code, system-prompt, capture-methods, debugging, anthropic-api, http-proxy]
sources: []
date: 2025-09-08
last_updated: 2026-04-07
---

## Summary

This document compares two working methods for capturing Claude Code's system prompt: the Debug Method using Claude CLI's built-in functionality, and an HTTP Proxy Method using a custom Python proxy. Both methods successfully captured the complete ~32KB system prompt that Claude Code sends to the Anthropic API.

## Key Claims

- **Debug Method Works**: `claude --debug api --dangerously-skip-permissions -p "Hello"` successfully captures the full system prompt with no external dependencies
- **HTTP Proxy Method Works**: Custom Python proxy intercepting API requests captures the system prompt in structured JSON format
- **ccproxy-api Failed**: Version 0.1.7 has Pydantic model compatibility issues that were not resolved
- **Identical Content**: Both methods capture identical ~32KB system prompt content, validating their accuracy
- **System Prompt Structure**: Two-part structure - basic identity (58 bytes) plus full behavioral instructions (~32KB)

## Key Quotes

> "Both working methods successfully captured the complete ~32KB system prompt that Claude Code sends to the Anthropic API."

> "System Prompt Structure: Part 1: Basic identity (58 bytes) - 'You are Claude Code, Anthropic's official CLI for Claude.' Part 2: Complete instructions (~32KB) - Full behavioral system prompt"

## Connections

- [[Claude Code System Prompt - Captured via Debug Mode]] — Related source showing the actual captured system prompt content

## Contradictions

- None identified