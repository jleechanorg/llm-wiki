---
title: "OpenClaw Provider Critical PR Review Tests"
type: source
tags: [python, testing, openclaw, gateway, provider, pr-review, bug-fix]
source_file: "raw/test_openclaw_provider_critical_pr_review.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Tests for six critical PR review comments in the OpenClaw provider. Covers gateway URL override bugs, variable initialization issues, JSON mode compatibility with alternative providers, streaming conversation handling, JSON enforcement for non-streaming calls, and provider model naming conventions.

## Key Claims
- **Gateway URL override**: gateway_port should NOT override explicit OPENCLAW_GATEWAY_URL — prevents breaking production and localhost SSRF vulnerabilities
- **Variable initialization**: resolved_user_id must be set before use in all code paths
- **JSON mode compatibility**: json_mode breaks Cerebras and OpenRouter providers — needs provider-specific handling
- **Streaming conversation structure**: Phase2 streaming destroys OpenClaw conversation structure — needs preserved state
- **Non-streaming JSON enforcement**: Non-streaming OpenClaw skips JSON enforcement — needs consistent JSON mode application
- **Provider model naming**: OpenClaw provider selection should use model="local" not openclaw/gemini-3-flash-preview

## Connections
- [[OpenClaw]] — The gateway being tested
- [[GatewayURLResolution]] — Related concept for URL override behavior
- [[JSONModeHandling]] — Related concept for JSON mode provider compatibility
