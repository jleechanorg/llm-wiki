---
title: "Architectural Boundaries"
type: concept
tags: [architecture, testing, api, protocol-boundary]
sources: [opaque-choice-ids-resolver-contract-2026-05-15]
last_updated: 2026-05-15
---

## Description
The conceptual separation between different layers of a software system. In WorldArchitect.AI, three key boundaries exist: Frontend → main.py (API Gateway), main.py → world_logic.py (MCP Protocol), and world_logic.py → Response (Business Logic).

## Key Principles
- **Field Format Consistency**: Error/success fields ("error"/"success") must be identical across all boundaries
- **Intentional Translation**: Different layers may use different field names (e.g., "input" vs "user_input") with explicit translation logic
- **Validation Testing**: RED-GREEN tests validate that field formats remain consistent and translation works correctly
- **Resolver Ownership**: For opaque choice IDs, schema and selected-choice resolver own semantic translation before correction guards run

## Connections
- [[ArchitecturalBoundaryFieldFormatValidation]] — tests for boundary validation
- [[OpaqueChoiceIdContract]] — choice-ID semantics boundary for planning choices
- [[main.py]] — API Gateway boundary
- [[world_logic.py]] — Business Logic boundary
