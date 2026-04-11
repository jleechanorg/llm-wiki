---
title: "MCP Interaction Structured Fields Tests"
type: source
tags: [python, testing, mcp, api, structured-data, interaction-endpoint]
source_file: "raw/test_mcp_interaction_structured_fields.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating structured field handling through the MCP API gateway interaction endpoint. Tests verify that interaction requests with various modes (character, combat) flow correctly through the MCP architecture and return appropriate responses.

## Key Claims
- **MCP gateway handles interaction requests**: The MCP API gateway correctly routes interaction requests to the appropriate endpoint
- **Structured response format**: Responses are returned as structured JSON dictionaries
- **Combat interaction support**: Combat scenarios with action inputs work through MCP
- **Data type handling**: Various data types (character sheets, inventory, abilities) are handled correctly
- **Authentication bypass**: Test headers (X-Test-Bypass-Auth, X-Test-User-ID) enable testing without real Firebase auth
- **Error handling**: Invalid campaigns return appropriate 404 errors

## Test Coverage
- Basic interaction requests with mode switching
- Structured response verification
- Combat scenario routing
- Data type verification

## Connections
- [[MCP]] — architecture being tested
- [[Firebase]] — authentication service used
- [[Flask]] — web framework under test
