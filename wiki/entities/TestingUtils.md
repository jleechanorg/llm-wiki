---
title: "TestingUtils"
type: entity
tags: [testing, python, module]
sources: [code-centralization-testing-utils-deduplication]
last_updated: 2026-04-08
---

Canonical testing utility module serving as the single source of truth for shared testing functions. Functions like `wait_for_server_healthy`, `get_next_iteration`, `generate_run_id`, `write_with_checksum`, and `create_checksum_for_file` are centralized here and imported by consumer modules (testing_mcp, testing_ui) rather than being re-implemented.

## Related Entities
- [[TestingMcp]] — consumer module
- [[TestingUi]] — consumer module
- [[BD5762]] — refactoring ticket
