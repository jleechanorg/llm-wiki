---
title: "Test Consolidation"
type: concept
tags: [testing, maintainability, optimization]
sources: [sariel-test-suite-consolidation]
last_updated: 2026-04-08
---

## Definition
Test consolidation is the practice of merging redundant, overlapping test files into a smaller set of focused, non-duplicative tests.

## Key Principles
- **Single responsibility**: Each test file has a distinct, non-overlapping purpose
- **Reduce duplication**: Remove tests that cover the same ground
- **Configurable depth**: Use environment variables to toggle between quick and comprehensive runs
- **Maintain clarity**: Make test intent obvious from file name and structure

## Benefits
- Fewer API calls (73-95% reduction in Sariel case)
- Faster execution time
- Easier maintenance — one place to update for a given test purpose
- Clearer test intent for new contributors

## Related Concepts
- [[APICallOptimization]] — reducing the number of external API calls in tests
- [[EnvironmentDrivenTesting]] — using env vars to configure test behavior
- [[DualModeTesting]] — running tests against mock or real backends
