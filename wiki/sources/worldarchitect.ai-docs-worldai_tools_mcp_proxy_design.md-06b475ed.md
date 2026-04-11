---
title: "WorldAI Tools MCP Proxy Design"
type: source
tags: [mcp, proxy, architecture, diagnostic, admin, ops, gcp, firebase, worldarchitect]
sources: []
date: 2026-03-03
source_file: WorldArchitect AI Docs - MCP Proxy Design
last_updated: 2026-04-07
---

## Summary
Design document for a WorldAI Tools MCP Proxy that exposes existing WorldAI MCP tools without tool-by-tool rewrites while adding safe diagnostic/admin tools for dice evaluation, campaign copy/download, and guardrailed GCP/Firebase operations. The proxy runs as its own MCP server with two layers: a passthrough layer that forwards to the real upstream MCP server, and a local tool layer hosting admin/diagnostic/ops tools.

## Key Claims
- **Passthrough Architecture**: Forwards unknown tools/resources to real WorldAI MCP server without individual tool rewrites, using tools/list merge and tools/call forward patterns
- **Local Admin Tools**: Diag tools for dice evaluation, campaign copy/download, campaign entry downloads with file written only to Downloads root
- **Guardrailed GCP/Firebase Ops**: Controlled tools for gcloud log reads, Firestore read/query helpers, and run/deploy controls for MCP services
- **Non-Goals**: No business logic changes, no broad Firestore write admin, no raw file content in responses
- **Grounded in Existing Files**: Design references mvp_site/mcp_api.py, mvp_site/mcp_client.py, firestore_service.py, and various scripts for existing patterns

## Connections
- [[MCP Architecture]] — related to WorldArchitect.AI's MCP-based tool system
- [[Firebase Operations]] — guarded Firestore operations via the proxy
- [[Campaign Management]] — campaign copy/download operations through proxy tools
