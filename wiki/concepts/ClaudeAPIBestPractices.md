---
title: "Claude API Best Practices"
type: concept
tags: [anthropic, claude, api, SDK, best-practices]
sources: [external-ai-knowledge-sources]
last_updated: 2026-04-14
---

## Summary

The Anthropic Claude API provides access to Claude models via REST and SDKs (Python, Node). Best practices span API design (caching, batching), cost optimization, safety configuration, and integration patterns for production applications.

## Key Claims

- **Prompt caching** (beta) is the single highest-impact optimization for applications with repeated system prompts — reduces cost and latency dramatically.
- Use `anthropic-beta: prompt-caching/2025-05-14` header to enable caching; set `cache_control` on system prompt and long examples.
- Max tokens must be set to allow full response; under-setting is the most common API error.
- Streaming (`stream: true`) improves perceived latency for user-facing applications even if total time is similar.
- The Messages API supports multi-turn conversations; maintain conversation history for context.

## SDK Best Practices

- **Python SDK** (`pip install anthropic`): use the `Anthropic` client with context manager for connection pooling.
- **Node SDK**: use async/await patterns; avoid creating new clients per request.
- Always set `timeout` on client construction; default may be too short for slow models.
- Handle `rate_limit_error` with exponential backoff; Anthropic returns `Retry-After` header.
- Use the count_tokens function to pre-validate context window budget before API call.

## Safety Configuration

- `max_tokens` also acts as a safety limit — set it to the maximum response size you can handle.
- Use `遏制` (custom stop sequences) to control when model stops generating.
- System prompt + user prompt together define behavior; keep system prompts in the `system` field, not user messages.
- For high-stakes applications, implement server-side output validation before downstream use.

## Cost Optimization

- Prompt caching: mark system prompt and few-shot examples with `cache_control: { type: "ephemeral" }`.
- Truncate long conversation histories before they approach context window limits — summarize older turns.
- Use Haiku for high-volume, lower-stakes tasks; reserve Opus for complex reasoning.
- Batch API (`/v1/messages/batches`) for offline processing of up to 10,000 messages per batch.

## Connections

- [[Prompt Engineering]] — API usage is how prompt engineering is operationalized
- [[RLHF]] — RLHF is the training technique behind Claude's helpfulness and harmlessness