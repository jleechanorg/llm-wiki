---
title: "OpenClaw HTTP Client"
type: source
tags: [python, http, client, openclaw, gateway, chat-completions, streaming]
source_file: "raw/openclaw-http-client.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python HTTP client for OpenClaw gateway providing OpenAI-compatible /v1/chat/completions interface. Supports streaming and non-streaming modes, token-based authentication, and configurable gateway URLs via environment variables.

## Key Claims
- **Gateway URL Resolution**: Supports explicit URL via OPENCLAW_GATEWAY_URL env var or builds from host/port defaults (127.0.0.1:18789)
- **Token Authentication**: Optional Bearer token via OPENCLAW_GATEWAY_TOKEN header
- **Streaming Support**: Generator-based streaming responses with event parsing (message, content, done)
- **System Instructions**: Prepends system message to message array for instruction injection
- **Model Name Handling**: Strips "openclaw/" prefix before forwarding to gateway
- **Response Extraction**: Parses OpenAI-style response format with choices[0].message.content
- **Error Propagation**: Captures gateway-level error field and raises as RuntimeError
- **Timeout Configuration**: 600s default request timeout, 8s connection test timeout (configurable)

## Key Code Patterns
```python
# Environment variable configuration
OPENCLAW_GATEWAY_URL=...    # Explicit full URL (trusted, no SSRF check)
OPENCLAW_GATEWAY_HOST=...   # Default 127.0.0.1
OPENCLAW_GATEWAY_PORT=...   # Default 18789
OPENCLAW_GATEWAY_TOKEN=...  # Bearer token for auth

# Usage
client = OpenClawHTTPClient(gateway_url=url, gateway_token=token)
response = client.invoke(messages=[...], model_name="openclaw/gpt-4o", ...)
```

## Connections
- [[OpenClawGateway]] — the gateway this client connects to
- [[OpenAICompatibleChatCompletions]] — shared core this builds upon
- [[TailscaleFunnel]] — used to expose local gateway publicly
- [[FirestoreSettings]] — where gateway URL/token may be stored for users

## Contradictions
- None detected
