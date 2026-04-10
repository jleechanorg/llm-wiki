---
title: "Provider Fallback"
type: concept
tags: [resilience, api, fallback]
sources: []
last_updated: 2026-04-08
---

System behavior where the application falls back to alternate LLM providers when the default provider fails or its API key is missing. For example, falling back to Cerebras when Gemini API key is not available.

## Implementation
The system checks for available API keys and gracefully switches providers rather than hard failing.

## Related Concepts
- [[Gemini]] — default provider
- [[Cerebras]] — fallback provider
