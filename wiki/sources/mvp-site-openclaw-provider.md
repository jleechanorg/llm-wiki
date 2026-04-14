---
title: "mvp_site openclaw_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/openclaw_provider.py
---

## Summary
OpenClaw gateway HTTP client for chat completions. Communicates with OpenClaw gateway running on localhost (default port 18789) for inference. Supports gateway URL/token configuration via environment variables.

## Key Claims
- OpenClawHTTPClient for gateway chat completions
- _get_gateway_url() reads OPENCLAW_GATEWAY_URL or constructs from HOST/PORT
- DEFAULT_GATEWAY_PORT = 18789, REQUEST_TIMEOUT_SECONDS = 600
- CONNECTION_TEST_TIMEOUT_SECONDS = 8 for gateway connectivity testing

## Connections
- [[LLMIntegration]] — OpenClaw gateway for inference
