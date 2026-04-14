---
title: "mvp_site openai_proxy_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/openai_proxy_provider.py
---

## Summary
OpenAI-compatible inference proxy forwarding requests to user's personal OpenClaw gateway. Flask server routes translated to user's gateway via Tailscale Funnel or Cloudflare Tunnel. worldai_ personal API keys resolve to user_id via Firestore.

## Key Claims
- External caller → POST /v1/chat/completions → user's OpenClaw gateway
- Auth: worldai_ personal API keys resolved to user_id via Firestore
- URL resolution: user's gateway_url + gateway_token from Firestore settings
- _safe_gateway_url_for_log() redacts user-controlled gateway URLs

## Connections
- [[LLMIntegration]] — proxy to OpenClaw gateway
