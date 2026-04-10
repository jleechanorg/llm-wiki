---
title: "Error Propagation"
type: concept
tags: [error-handling, mcp, testing]
sources: ["mcp-error-handling-e2e-tests"]
last_updated: 2026-04-08
---

## Definition
The pattern of errors flowing through multiple layers of an application stack, being translated and transformed at each boundary. In this test suite, errors originate in world_logic, pass through MCPClient, and are translated into proper Flask HTTP responses.

## Error Types Tested
- **Campaign not found** (404) — non-existent campaign ID
- **Authentication errors** (401/403) — missing or invalid user credentials
- **Request validation errors** (400) — malformed JSON, missing required fields
- **Interaction errors** — operations on non-existent resources

## Related Concepts
- [[ErrorHandling]] — broader discipline of handling exceptions
- [[HTTPStatusCodes]] — standardized error code system
- [[MCPClient]] — layer responsible for error translation
