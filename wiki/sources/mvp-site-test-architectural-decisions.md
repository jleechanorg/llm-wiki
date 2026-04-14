---
title: "test_architectural_decisions.py"
type: source
tags: [test, architecture, pydantic, validation]
date: 2026-04-14
source_file: raw/mvp_site_all/test_architectural_decisions.py
---

## Summary
Test suite that validates architectural decisions remain implemented as designed. Covers ADT-001 through ADT-020, verifying Pydantic validation is used exclusively, defensive numeric conversion works, and the AST-based architecture analysis engine functions correctly.

## Key Claims
- ADT-001: Entity validation uses Pydantic implementation exclusively
- ADT-002: Only Pydantic implementation exists (Simple version removed)
- ADT-003: entity_tracking.py imports from Pydantic module
- ADT-004: Pydantic validation rejects invalid data (e.g., gender required for NPCs)
- ADT-005: DefensiveNumericConverter handles 'unknown' values gracefully
- ADT-006: No environment variable switching - Pydantic always used
- ADT-007 to ADT-020: AST analysis engine validates architecture

## Key Quotes
> "These tests verify that our architectural decisions remain valid and are actually implemented as designed. They prevent the 'test name vs reality' problem."

## Connections
- [[EntityTracking]] — imports from entities_pydantic module
- [[PydanticValidation]] — core validation implementation
- [[DefensiveNumericConverter]] — handles unknown/missing values

## Contradictions
- None identified in this test file