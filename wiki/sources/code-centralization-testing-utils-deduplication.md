---
title: "Code Centralization Testing Utils Deduplication"
type: source
tags: [testing, python, code-centralization, deduplication, refactoring]
source_file: "raw/code-centralization-testing-utils-deduplication.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Tests verifying code centralization into testing_utils. RED phase tests assert that duplicate functions have been removed from consumer modules (testing_mcp, testing_ui) and replaced with delegations to the canonical testing_utils implementations.

## Key Claims
- **_wait_for_server_ready Removal**: `_wait_for_server_ready` must be removed from testing_mcp/lib/server_utils and replaced with delegation to `wait_for_server_healthy` from testing_utils.server
- **Evidence Utils Delegation**: Generic evidence functions (`_get_next_iteration`, `_generate_run_id`, `write_with_checksum`, `create_checksum_for_file`) must be imported from testing_utils.evidence, not re-implemented
- **No Subprocess Reimplementation**: Functions like `get_current_branch_name` must not contain their own subprocess calls; they should delegate to testing_utils
- **Centralized Redaction**: `save_request_responses` should use centralized credential redaction from testing_utils

## Connections
- [[TestingUtils]] — canonical module receiving centralized functions
- [[TestingMcp]] — consumer module being refactored
- [[TestingUi]] — consumer module being refactored
- [[BD5762]] — ticket driving this deduplication work

## Contradictions
- None identified
