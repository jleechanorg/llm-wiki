---
title: "RED-GREEN Test: Architectural Boundary Field Format Validation"
type: source
tags: [python, testing, unittest, architecture, api, boundary-testing]
source_file: "raw/architectural-boundary-field-format-validation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest validating field format consistency across three architectural boundaries: Frontend → main.py (API Gateway), main.py → world_logic.py (MCP Protocol), and world_logic.py → Response (Business Logic). Tests confirm intentional translation patterns like `input` → `user_input` and validate error/success field consistency.

## Key Claims
- **Frontend → main.py**: Uses "input" field for frontend compatibility
- **main.py → world_logic.py**: Uses "user_input" field for MCP protocol
- **Field Translation**: Intentional conversion between formats at translation layer
- **Cross-Boundary Consistency**: Error/success fields ("error"/"success") consistent across all boundaries
- **Story Fields**: Must use "text" format for UI display

## Key Test Cases
1. `test_frontend_to_main_field_constants` - Validates "input" field and standard response fields
2. `test_main_to_mcp_field_constants` - Validates "user_input" field for MCP protocol
3. `test_mcp_api_field_constants` - Validates MCP API layer field consistency
4. `test_cross_boundary_field_consistency` - Validates error/success fields identical across layers
5. `test_translation_layer_field_conversion` - Confirms intentional "input" → "user_input" translation

## Connections
- [[main.py]] — API Gateway handling frontend requests
- [[world_logic.py]] — Business logic with MCP protocol
- [[mcp_api.py]] — MCP API layer for protocol handling
- [[ArchitecturalBoundaries]] — Concept for API boundary testing

## Contradictions
- None identified
