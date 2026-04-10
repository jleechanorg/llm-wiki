---
title: "Test Client Pattern"
type: concept
tags: [testing, pattern, client, automation]
sources: []
last_updated: 2026-04-08
---

## Description
A test client is a lightweight, programmatic interface for verifying server functionality without requiring a full application stack. Test clients typically provide:

- Direct HTTP/RPC access to server endpoints
- Health check methods for availability verification
- Request/response logging for debugging
- Method builders for constructing valid requests

## MCP Test Client
The MCPTestClient implements this pattern for WorldArchitect.AI:
- Instantiates with base_url and optional log_file
- Methods map to server capabilities (health, tools, resources, custom calls)
- JSON logging enables post-mortem debugging of test failures

## Related Patterns
- Fake/test doubles — mock services for unit tests
- End-to-end testing — full integration verification
