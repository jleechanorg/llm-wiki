---
title: "TestingMcp"
type: entity
tags: [testing, python, module]
sources: [code-centralization-testing-utils-deduplication]
last_updated: 2026-04-08
---

Testing module for MCP (Model Context Protocol) functionality. Being refactored to remove duplicate implementations of generic testing utilities, delegating instead to [TestingUtils](TestingUtils.md).

## Functions Being Centralized
- `_wait_for_server_ready` → `wait_for_server_healthy` from testing_utils.server
- Evidence utility functions → testing_utils.evidence

## Related Entities
- [TestingUtils](TestingUtils.md) — canonical module
- [TestingUi](TestingUi.md) — sibling consumer module
- [BD5762](BD5762.md) — refactoring ticket
