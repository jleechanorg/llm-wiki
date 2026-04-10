---
title: "Tool Schema"
type: concept
tags: [json-schema, tools, llm, contract]
sources: []
last_updated: 2026-04-08
---

JSON Schema defining the expected structure of tool/function call responses from LLMs. In WorldArchitect.AI, the narrative_response_schema defines how the LLM should format its narrative output for consistent parsing.

## Example: Narrative Response Schema
The schema specifies:
- Response format (JSON object)
- Required fields for narrative content
- Type definitions for game state updates
- Error handling patterns

## Related Concepts
- [[JSONSchemaDocumentationGenerator]] — utility for generating schema documentation
- [[MCPClientLibraryforWorldArchitectAI]] — parses tool call responses using schema
- [[ContractManifest]] — tracks tool schema versions
