---
title: "Gateway"
type: concept
tags: [api, proxy, openai-compatible]
sources: []
last_updated: 2026-04-08
---

A gateway in this context is a local server that provides an OpenAI-compatible /v1/chat/completions API. OpenClaw gateway runs on port 18789 and translates requests to whichever backend LLM the user has configured.

## Related Pages
- [[OpenClaw HTTP Client]] — Python client for gateway communication
- [[OpenAI-Compatible Inference Proxy]] — Server-side proxy forwarding to user gateways
