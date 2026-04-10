---
title: "Gateway URL Resolution"
type: concept
tags: [openclaw, gateway, configuration, security]
sources: []
last_updated: 2026-04-08
---

The process of determining the gateway URL for OpenClaw provider. When OPENCLAW_GATEWAY_URL is explicitly set to a non-local endpoint, gateway_port should NOT override it.

## Security Concern
- Prevents localhost SSRF where user-controlled port could redirect to malicious local services
- Preserves production setups where OPENCLAW_GATEWAY_URL points to a remote gateway

## Behavior
- Explicit URL takes precedence over port configuration
- Default localhost used only when no explicit URL is set
- Runtime environment variable reading required for test isolation
