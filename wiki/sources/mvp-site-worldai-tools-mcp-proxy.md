---
title: "mvp_site worldai_tools_mcp_proxy"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/worldai_tools_mcp_proxy.py
---

## Summary
WorldAI Tools MCP Proxy exposing local diagnostic/admin/ops MCP tools and forwarding other tools to upstream WorldAI MCP server. Provides diag_evaluate_campaign_dice and other local tools.

## Key Claims
- WorldAIToolsProxy handles routing between local and upstream tools
- RESERVED_PREFIXES = ("diag_", "admin_", "ops_") for local tool routing
- ALLOWED_FIRESTORE_OPS for Firestore query operation validation
- SENSITIVE_FIELD_PATTERN for field redaction
- MAX_REQUEST_SIZE = 10MB configurable via WORLDTOOLS_PROXY_MAX_CONTENT_LENGTH

## Connections
- [[MCPApi]] — local/remote tool routing
