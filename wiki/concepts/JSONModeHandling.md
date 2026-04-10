---
title: "JSON Mode Handling"
type: concept
tags: [json, llm-providers, cerebras, openrouter, compatibility]
sources: []
last_updated: 2026-04-08
---

JSON mode enforcement in LLM provider calls. Different providers have different JSON mode capabilities.

## Provider Compatibility
- **Cerebras**: Does not support JSON mode — breaks when enabled
- **OpenRouter**: Does not support JSON mode — breaks when enabled
- **OpenClaw**: Supports JSON mode via response_format parameter

## Best Practice
- Check provider capabilities before enabling JSON mode
- Fall back to text parsing for incompatible providers
