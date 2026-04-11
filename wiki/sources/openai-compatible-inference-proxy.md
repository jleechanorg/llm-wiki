---
title: "OpenAI-Compatible Inference Proxy"
type: source
tags: [python, flask, api, openai, proxy, openclaw, ssrf]
source_file: "raw/openai-compatible-inference-proxy.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Flask server providing OpenAI-compatible /v1/chat/completions endpoint that forwards requests to each user's personal OpenClaw gateway via Tailscale Funnel or Cloudflare Tunnel. Uses worldai_ personal API keys for authentication, resolved to user_id via Firestore.

## Key Claims
- **External Routing**: External CLI tools and applications can call this proxy to reach user's gateway
- **Auth Mechanism**: worldai_ personal API keys resolve to user_id via Firestore (same as /mcp endpoint)
- **URL Resolution**: User's gateway_url and gateway_token retrieved from Firestore settings
- **SSRF Protection**: Detects and rejects redirects to prevent gateway URL bypass attacks
- **Rate Limiting**: Configurable rate limits via environment variables (default 2000/hour, 200/minute)

## Key Components
- `_safe_gateway_url_for_log()` — redacts user-controlled URLs for safe logging
- `_reject_if_gateway_redirect()` — blocks redirect responses (SSRF bypass attempts)
- `ProxyPayload` dataclass — validated OpenAI chat completions payload
- `parse_chat_completions_payload()` — validates and extracts request body fields
- `post_chat_completions()` — forwards validated requests to user's gateway

## Security Considerations
- SSRF protection via redirect detection
- Maximum tokens cap (8192 default) to prevent runaway costs
- User-controlled URL redacted in logs (host:port only, no path/credentials)

## Connections
- [[OpenClaw]] — the user's personal inference gateway this proxy forwards to
- [[Firestore]] — user settings storage for gateway_url and gateway_token
- [[Flask]] — web framework powering this proxy server
