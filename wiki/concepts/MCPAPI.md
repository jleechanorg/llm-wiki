---
title: "MCP API"
type: concept
tags: [api, mcp, tools, integration]
sources: []
last_updated: 2026-04-08
---

Model Context Protocol API implementation for WorldArchitect.AI. The mcp_api_tool_contract defines the tool interface version 1.0.2, enabling the Flask server to expose MCP tools to the LLM.

## Contract Details
- **Version**: 1.0.2
- **Path**: mvp_site/mcp_api.py
- **Purpose**: Define tool interface contract for LLM function calling

## Related Pages
- [[MCPClientLibraryforWorldArchitectAI]] — JSON-RPC 2.0 client with HTTP-to-MCP translation
- [[PromptContractManifest]] — tracks MCP API contract version
- [[OpenAICompatibleInferenceProxy]] — Flask server forwarding to user gateways
