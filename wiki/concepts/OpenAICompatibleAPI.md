---
title: "OpenAI Compatible API"
type: concept
tags: [api, openai, standard, proxy]
sources: []
last_updated: 2026-04-08
---

## Definition
An API interface that replicates the OpenAI chat completions format, allowing compatibility with OpenAI client libraries and tools while routing requests to alternative model providers.

## Key Components
- **/v1/chat/completions** — the main endpoint for chat-based text generation
- **/v1/models** — endpoint for listing available models
- Standard payload format: { model, messages, temperature, max_tokens, stream, tools, response_format }

## Usage in This Project
The OpenClaw proxy implementation at mvp_site.llm_providers.openai_proxy_provider provides an OpenAI-compatible interface that forwards requests to a configurable gateway URL, enabling use of alternative LLM providers while maintaining OpenAI client compatibility.

## Related Concepts
- [[ChatCompletions]] — the specific endpoint for conversational text generation
- [[GatewayForwarding]] — pattern of routing requests through a proxy layer
