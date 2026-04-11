---
title: "Integration Test Runner with Real API Calls"
type: source
tags: [testing, integration, api, bash, worldai]
source_file: "raw/integration-test-runner-real-api-calls.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Bash script that executes integration tests requiring live API connections to Google Gemini and Firebase Firestore. Tests are discovered from the `test_integration/` directory using Python's unittest framework. These tests are explicitly excluded from GitHub Actions CI due to their external service dependencies.

## Key Claims
- **Real API Dependencies** — Tests call actual Google Gemini API and Firebase Firestore
- **Environment Requirements** — Requires `GEMINI_API_KEY` env var and `serviceAccountKey.json` in project root
- **CI Exclusion** — Tests are excluded from GitHub Actions because they cannot run in isolated CI environments
- **Test Discovery** — Uses `find test_integration -name "test_*.py"` pattern for automatic test detection
- **Unittest Framework** — Runs tests via `python -m unittest` with exit code tracking

## Key Code Elements
- Test directory: `test_integration/`
- Test file pattern: `test_*.py`
- Authentication bypass: `TESTING_AUTH_BYPASS=true`
- Exit codes: 0 for success, 1 for failure
- Summary output: "$passed/$total tests passed"

## Connections
- [[PytestConfiguration]] — Alternative test runner for CI environments
- [[RealServiceProviderImplementation]] — Real Firestore/Gemini provider with capture mode
- [[PytestIntegrationRealModeTestingFramework]] — pytest fixtures for dual-mode testing

## Contradictions
- None identified
