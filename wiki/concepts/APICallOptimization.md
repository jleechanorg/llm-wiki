---
title: "API Call Optimization"
type: concept
tags: [testing, optimization, api]
sources: [sariel-test-files-analysis, sariel-test-suite-consolidation]
last_updated: 2026-04-08
---

## Description
Reducing the number of API calls in test files through consolidation while maintaining test coverage. The Sariel test suite achieved 73-95% reduction in API calls.

## Key Metrics
| Metric | Before | After | Reduction |
|--------|--------|-------|----------|
| Default test calls | 21 | 4 | 81% |
| Full test calls | 21 | 11 | 48% |
| Redundant files | 6 | 3 | 50% |

## Techniques
- Environment variable configuration
- Removing redundant state checks
- Combining validation and logging modes
-limiting interaction count for fast tests

## Connections
- [[TestSarielConsolidated]] — implementation
- [[SarielTestSuiteConsolidation]] — prior work
