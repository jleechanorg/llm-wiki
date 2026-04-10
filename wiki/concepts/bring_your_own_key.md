---
title: "BYOK (Bring Your Own Key)"
type: concept
tags: [api, authentication, llm]
sources: ["openrouter-provider-implementation"]
last_updated: 2026-04-08
---

Pattern where users provide their own API keys to a service rather than the service providing keys. In OpenRouter context, allows customers to use their own OpenRouter API key instead of the service's key, enabling custom billing and rate limiting.

## Implementation
- **Parameter**: api_key argument in generate_content()
- **Fallback**: Falls back to OPENROUTER_API_KEY env var if not provided
- **Use Case**: Multi-tenant applications, customer-managed quotas

## Connected Sources
- [[OpenRouter Provider Implementation]] — documents effective_api_key resolution

## Related Concepts
- [[OpenAI-Compatible API]] — authentication via Authorization header
