---
title: "TDD Tests for capture_provenance test_file Parameter"
type: source
tags: [python, testing, unittest, tdd, provenance, capture]
source_file: "raw/tdd-tests-capture-provenance-test-file.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest suite verifying that test_file parameter is properly defined and passed to capture_provenance() in MCPTestBase. Includes RED-phase test that should fail before fix is applied, validating TDD methodology.


## Key Claims
- **test_file Definition**: test_file must be defined before calling capture_provenance()
- **test_file Path**: test_file should point to the test class Python file
- **capture_provenance Call**: capture_provenance should be called with test_file in kwargs
- **External Server Client**: _create_external_server_client should be centralized

## Connections
- [[MCPTestBase]] — class under test
- [[capture_provenance]] — function being validated
