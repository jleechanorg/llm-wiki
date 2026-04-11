---
title: "WorldArchitect.AI Code Coverage Report — mvp_site Module Analysis"
type: source
tags: [code-coverage, testing, python, mvp-site, worldarchitect]
source_file: "raw/coverage-report-mvp-site.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Code coverage analysis of the WorldArchitect.AI mvp_site Python module revealing significant testing gaps. The 56-file module contains 7,000+ statements across core services (gemini_service, firestore_service, main) with 0% coverage at capture time, indicating no unit or integration tests executed against the production codebase.

## Key Claims
- **Zero Coverage**: All 56 Python files show 0% coverage, indicating no test execution against the codebase at capture time
- **Core Service Complexity**: gemini_service.py (822 statements), firestore_service.py (503 statements), and main.py (483 statements) represent the highest complexity areas
- **Testing Framework Present**: Separate testing_framework/ directory exists with 1,500+ lines but not integrated with mvp_site test execution
- **Mock Infrastructure**: Complete mock implementations exist for firestore_service and gemini_service but unused
- **Module Count**: 56 Python files in mvp_site core module, excluding mocks and testing_framework

## Key Quotes
> "gemini_service.py — 822 statements, 0% coverage" — largest single module by LOC
> "firestore_service.py — 503 statements, 0% coverage" — Firebase integration layer

## Connections
- [[TestingFramework]] — separate testing infrastructure not integrated with mvp_site
- [[MockFirestoreService]] — mock implementation exists but unused in test runs
- [[MockGeminiService]] — mock implementation exists but unused in test runs
- [[CaptureFramework]] — data capture framework for recording API interactions

## Contradictions
- [[PytestConfigurationForMVPSiteTests]] on: pytest configuration exists but coverage shows zero test execution
- [[TestConfigurationManagement]] on: test environment validation documented but not reflected in coverage data
