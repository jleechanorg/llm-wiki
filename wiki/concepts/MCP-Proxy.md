---
title: "MCP Proxy"
type: concept
tags: [mcp, proxy, architecture]
sources: [worldai-tools-mcp-proxy-tests]
last_updated: 2026-04-08
---

## Description
Model Context Protocol (MCP) proxy pattern that provides a secure gateway to MCP tool implementations. The [[WorldAIToolsProxy]] class implements this pattern for WorldAI tools.

## Key Features
- JSON-RPC 2.0 interface for tool invocation
- Authorization layer checking actor roles
- Input validation and sanitization
- Deploy confirm token verification

## Use Case
Securely expose WorldAI MCP tools (dice evaluation, campaign management, Firestore operations, Cloud Run deployments) to clients with proper authorization checks.
