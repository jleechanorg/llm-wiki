---
title: "API Test Consolidation Summary"
type: source
tags: [testing, api, optimization, test-automation, configuration-driven]
source_file: "raw/api-test-consolidation-summary.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Analysis of API test consolidation efforts resulting in 94% reduction in API calls for regular test runs. Removed redundant tests saving ~108 API calls, moved full validation to manual testing saving ~130 API calls, while preserving essential tests with configurable API call counts.

## Key Claims
- **Redundant Test Removal**: Removed 4 test files saving ~108 API calls (test_sariel_single_campaign_full.py, test_sariel_with_prompts.py, test_sariel_production_validation.py, test_sariel_production_flow.py)
- **Manual Testing Migration**: Moved 2 test files to manual testing saving ~130 API calls from regular runs (test_sariel_full_validation.py, test_sariel_exact_production.py)
- **Regular Run Reduction**: ~178 API calls → ~10-20 API calls (94% reduction)
- **Full Test Configuration**: SARIEL_FULL_TEST=true enables ~30 API calls for comprehensive validation
- **Configuration Options**: Multiple env vars for selective testing (TESTING_AUTH_BYPASS, SARIEL_DEBUG_PROMPTS, SARIEL_REPLAYS)

## Configuration Options
| Variable | Purpose | Default |
|---------|---------|---------|
| TESTING_AUTH_BYPASS | Skip auth | false |
| SARIEL_FULL_TEST | Full validation | false |
| SARIEL_DEBUG_PROMPTS | Debug prompt output | false |
| SARIEL_REPLAYS | Multiple replays | 1 |

## Connections
- [[TestSarielConsolidated]] — Main consolidated test file
- [[TestSarielProductionMethods]] — Production method validation
- [[TestIntegration]] — Core integration testing
