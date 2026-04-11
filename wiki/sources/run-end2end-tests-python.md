---
title: "End-to-End Integration Test Runner"
type: source
tags: [testing, integration, python, unittest, worldai]
source_file: "raw/run-end2end-tests-python.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python unittest-based runner script for executing end-to-end integration tests in the WorldAI MVP site. Tests run with mocked external services (Firestore & Gemini) and verify the full application flow through all layers.

## Key Claims
- **Full Stack Testing** — Tests the complete application flow through all layers, not just unit-level components
- **Mock External Services** — Only Firestore and Gemini are mocked; all other components run real code
- **Unittest Discovery** — Uses Python's unittest framework with automatic test discovery from test files

## Key Code Elements
- Test directory: `mvp_site/tests/`
- Discovery pattern: `test_*.py` files
- Verbosity: 2 (detailed output)
- Exit code: 0 for success, 1 for failure

## Connections
- [[PytestConfiguration]] — Alternative test runner (pytest-based)
- [[MockServiceProviderImplementation]] — Mock implementations used for testing
- [[PytestIntegrationRealModeTestingFramework]] — Dual-mode testing framework

## Contradictions
- None identified
