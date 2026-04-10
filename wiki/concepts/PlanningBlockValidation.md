---
title: "Planning Block Validation"
type: concept
tags: [validation, planning-block, structured-response]
sources: [planning-block-validation-integration-tests, test-planning-block-robustness-edge-cases, planning-block-choices-canonical-list, frontend-json-planning-block-tests]
last_updated: 2026-04-08
---

## Description
The process of validating that planning blocks in LLM responses conform to the required JSON structure. The `_validate_and_enforce_planning_block` function enforces JSON-only format and rejects legacy string formats.

## Validation Rules
- **Required fields**: `thinking` (string) and `choices` (dict/list)
- **Format**: Only JSON dict format supported, strings rejected
- **Type enforcement**: Integer and list planning blocks are rejected

## Server Warnings
Server-side warnings are stored in `_server_system_warnings` (not `system_warnings`) to prevent LLM spoofing while allowing legitimate server-generated warnings.

## Connections
- Validated by [[PlanningBlockValidationIntegrationTests]]
- Related to [[PlanningBlockListCanonicalization]]
