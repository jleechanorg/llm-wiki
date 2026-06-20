---
title: "Unified API Pattern"
type: concept
tags: [architecture, api, design-pattern]
sources: [unified-api-implementation]
last_updated: 2026-04-08
---

## Definition
Software architecture pattern where a single business logic layer serves multiple interface layers (e.g., REST API, MCP tools, CLI). Centralizes core functionality while exposing multiple access points.

## Application
In WorldArchitect.AI, the [UnifiedApiPy](../entities/UnifiedApiPy.md) module serves both [Flask](Flask.md) routes and [MCPServer](../entities/MCPServer.md) tools, eliminating duplicated business logic.

## Benefits
- Code reuse: business logic implemented once
- Consistency: same JSON formats across interfaces
- Maintainability: single source of truth
- Testability: test business logic once

## Related Concepts
- [BusinessLogicExtraction](BusinessLogicExtraction.md)
- [JSONSchemaStandardization](JSONSchemaStandardization.md)
- [[InterfaceSegregation]]
