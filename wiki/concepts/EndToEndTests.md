---
title: "End-to-End Tests"
type: concept
tags: [testing, e2e, integration]
sources: [mvp-test-optimization-recommendations]
last_updated: 2026-04-08
---

## Definition
End-to-end (E2E) tests validate entire application workflows from start to finish, testing multiple components together as they would function in production.

## Characteristics
- Test full user journeys (e.g., campaign creation, story continuation)
- Use real or mocked external services
- Slower than unit tests but higher confidence
- Cover integration points between components

## Role in Test Suite
The MVP test suite includes 4,544 lines of e2e tests covering:
- Campaign CRUD operations
- Debug and god mode settings
- MCP protocol compliance
- Entity tracking and memory budgets
- Narrative JSON cleanup

These tests serve as the baseline for identifying redundant unit tests that can be trimmed or deleted.
