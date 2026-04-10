---
title: "Configuration-Driven Testing"
type: concept
tags: [testing, configuration, automation, optimization]
sources: [api-test-consolidation-summary]
last_updated: 2026-04-08
---

Testing methodology where test scope, depth, and API call volume is controlled via environment variables rather than separate test files. Enables single test file to serve multiple purposes from quick validation to comprehensive testing.

## Benefits
- Single test file replaces multiple redundant files
- API call volume scales with configuration
- Selective feature testing via flags
- Manual/full testing available on-demand

## Example Variables
- TESTING_AUTH_BYPASS: Skip authentication
- SARIEL_FULL_TEST: Enable full validation suite
- SARIEL_DEBUG_PROMPTS: Output debugging info
- SARIEL_REPLAYS: Run multiple iterations
