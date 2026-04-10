---
title: "MCP (Model Context Protocol)"
type: concept
tags: [mcp, protocol, ai, tools]
sources: [worldai-tools-mcp-proxy-runtime, worldai-mcp-stdio-adapter]
last_updated: 2026-04-08
---

MCP (Model Context Protocol) is a standardized protocol for AI systems to expose tools and resources to language models. The WorldAI wiki documents two MCP implementations:

1. **WorldAI MCP STDIO Adapter** — stdio-based server reading JSON-RPC from stdin
2. **WorldAI Tools MCP Proxy Runtime** — HTTP server-based with local tool exposure and upstream forwarding

## Key Patterns
- Tool registration with inputSchema definitions
- JSON-RPC 2.0 message format
- Authentication context propagation
- Resource catalog exposure

## Related
- [[JSON-RPC 2.0]]
- [[WorldAI MCP STDIO Adapter]]
- [[WorldAI Tools MCP Proxy Runtime]]
