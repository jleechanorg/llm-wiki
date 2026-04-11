---
title: "Schema Test Centralization Evidence"
type: source
tags: [schema-validation, testing, error-classification, test-centralization, firestore]
source_file: "raw/worldarchitect.ai-schema-test-centralization-evidence.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Successfully implemented error/warning classification in schema validation tests, enabling tests to distinguish between blocking errors (test failures) and non-blocking warnings (informational). Test now shows 100% pass rate when only non-blocking warnings are present.

## Key Claims
- **Problem**: test_schema_enforcement_journey_real_api.py showed 0% pass rate due to schema validation warnings being treated as failures
- **Solution**: SchemaValidationTestBase with is_blocking_error() to classify blocking vs non-blocking errors
- **Evidence**: 100% pass rate (1/1 tests) with 22 warnings but 0 blocking errors
- **Files**: testing_mcp/lib/schema_test_base.py (369 lines), testing_mcp/lib/component_validation_test_base.py (205 lines)

## Key Quotes
> "No distinction between blocking errors - Type/format violations that should fail tests - and non-blocking warnings - Structural issues (e.g., oneOf/anyOf mismatches) that are informational"

## Connections
- [[SchemaValidationTestBase]] — base class for schema validation tests
- [[ComponentValidationTestBase]] — base class for component-level validators
- [[PR4534]] — the PR that implemented this fix

## Contradictions
- None identified
