---
title: "MCPClient"
type: entity
tags: [python, client, mcp, error-handling]
sources: ["mcp-error-handling-e2e-tests"]
last_updated: 2026-04-08
---

## Description
Python client class that handles communication with the Model Context Protocol (MCP) server. Translates errors from world_logic through to Flask HTTP responses.

## Role in System
- Acts as middleware layer between application logic and HTTP endpoints
- Translates errors from world_logic into proper HTTP responses
- Handles error propagation through the MCP layer

## Related Pages
- [[MCPErrorHandlingE2E]] — tests error translation through MCPClient
- [[Flask]] — HTTP response layer receiving translated errors
- [[world_logic]] — source of errors that flow through MCPClient
