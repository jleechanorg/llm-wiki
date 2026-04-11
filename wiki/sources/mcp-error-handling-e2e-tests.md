---
title: "MCP Error Handling End-to-End Tests"
type: source
tags: [python, testing, e2e, mcp, error-handling]
source_file: "raw/test_mcp_error_handling_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test suite validating error propagation from world_logic through MCPClient to Flask HTTP responses. Only mocks external services (Firestore DB and Gemini API) at the lowest level, testing the full application stack error translation.

## Key Claims
- **Error propagation chain**: Tests verify errors flow correctly from world_logic → MCPClient → Flask HTTP responses
- **Campaign not found handling**: Tests MCP error translation for non-existent campaigns returning proper 404
- **Authentication error handling**: Tests MCP error translation for missing user ID returning 401/403
- **Request format validation**: Tests MCP error translation for invalid JSON and missing required fields
- **Interaction endpoint error handling**: Tests interaction with non-existent campaign returns proper error

## Key Quotes
> "End-to-end integration test for MCP error handling and translation. Tests error propagation from world_logic → MCPClient → Flask HTTP responses."

## Connections
- [[MCPClient]] — client translating errors through the MCP layer
- [[FakeFirestoreClient]] — test mock for Firestore database
- [[Flask]] — HTTP response layer for error translation
- [[world_logic]] — source of errors in the propagation chain
- [[FirestoreService]] — backend service whose errors are translated

## Contradictions
- None identified
