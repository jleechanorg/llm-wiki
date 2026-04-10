---
title: "Integration Testing"
type: concept
tags: [testing, integration, validation, logging]
sources: [planning-block-validation-integration-tests]
last_updated: 2026-04-08
---

## Description
A testing approach that validates the complete flow of functions including all code paths, dependencies, and side effects. Integration tests for planning block validation test the full flow from input through logging to output.

## Key Characteristics
- Tests multiple components working together
- Validates logging paths (warning, error, info)
- Tests crash safety with malformed inputs
- Verifies state changes on structured response objects

## Connections
- Different from [[UnitTesting]] which tests individual functions in isolation
- Used in [[MCPErrorHandlingE2E]] and [[MissionAutoCompletionE2E]] workflows
