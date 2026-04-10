---
title: "WorldAIToolsProxy"
type: entity
tags: [python, mcp, proxy, worldai]
sources: [worldai-tools-mcp-proxy-runtime]
last_updated: 2026-04-08
---

WorldAIToolsProxy is a Python class that provides the actual MCP tool handling logic for the WorldAI Tools MCP Proxy. The proxy wraps this class to add stdio/HTTP server I/O handling while delegating tool execution to the underlying proxy implementation.

## Key Responsibilities
- Tool catalog management and exposure
- Authentication context building
- Upstream MCP server forwarding

## Related
- [[WorldAI Tools MCP Proxy Runtime]] — wraps this class
- [[WorldAI MCP STDIO Adapter]] — similar wrapper pattern with stdio I/O
