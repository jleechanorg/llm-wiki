---
title: "Mock Patching"
type: concept
tags: [testing, mocking, unittest]
sources: [faction-tools-schema-execution-unit-tests]
last_updated: 2026-04-08
---

## Definition
A unittest technique using `unittest.mock.patch` to replace backend functions with mock objects during testing. Enables testing tool execution logic in isolation from actual implementation.

## Application
Tests patch functions like `calculate_faction_power` and `calculate_ranking` to return controlled values, verifying the tool execution layer correctly passes parameters and returns results.

## Related Concepts
- [[ToolSchemaValidation]] — what these tests validate
- [[ToolExecutionMapping]] — what mock patches enable testing
