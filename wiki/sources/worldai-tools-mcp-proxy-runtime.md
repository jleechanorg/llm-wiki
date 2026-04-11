---
title: "WorldAI Tools MCP Proxy Runtime"
type: source
tags: [python, mcp, proxy, json-rpc, http, diagnostics]
source_file: raw/worldai_tools_mcp_proxy_runtime.py
sources: []
last_updated: 2026-04-08
---

## Summary
Python service exposing local diagnostic/admin/ops MCP tools via stdio while forwarding all other requests to an upstream WorldAI MCP server. Provides admin operations for campaign management, Firestore querying, and Google Cloud Logging access with environment-driven configuration and authentication context building.

## Key Claims
- **Local + Remote Tool Split**: Exposes local tools with `diag_`, `admin_`, `ops_` prefixes while proxying other requests upstream
- **Deploy Token Security**: Validates deploy confirmation tokens with age limits (600s default) and future skew protection (120s)
- **Sensitive Data Redaction**: Filters authorization, token, api_key, secret fields from logs via regex pattern matching
- **Firestore Query Allowlisting**: Restricts Firestore operations to safe comparison operators only
- **GCloud Command Validation**: Validates service names match `^[a-z0-9_-]+$` pattern for security

## Key Functions
- `diag_evaluate_campaign_dice`: Evaluate campaign dice telemetry
- `admin_copy_campaign_user_to_user`: Copy campaign between users
- `admin_download_campaign`: Download campaign artifacts
- `admin_download_campaign_entries`: Download story entries as JSON/JSONL
- `ops_gcloud_logs_read`: Read Cloud Logging entries

## Connections
- [[WorldAIToolsProxy]] — wrapped for actual MCP logic
- [[WorldAI MCP STDIO Adapter]] — different adapter pattern (stdio vs HTTP server)
- [[Firestore]] — admin operations target
- [[Google Cloud Logging]] — accessed via gcloud wrapper

## Contradictions
- None identified
