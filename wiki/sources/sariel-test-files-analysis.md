---
title: "Sariel Test Files Analysis"
type: source
tags: [testing, sariel, api-calls, test-consolidation]
source_file: "raw/sariel-test-files-analysis.md"
sources: [sariel-campaign-replay-desync-measurement, sariel-test-suite-consolidation]
last_updated: 2026-04-08
---

## Summary
Analysis of 6 Sariel test files documenting API call patterns, redundancy identification, and consolidation recommendations. Shows progression from 21 API calls per test to consolidated 4-11 calls depending on configuration.

## Key Claims
- **6 Test Files Analyzed** — various purposes from single campaign runs to full validation with 110 API calls
- **Consolidation Achieved** — test_sariel_consolidated.py reduces calls 73-95% vs original tests
- **Default Configuration: 4 API Calls** — 1 campaign creation + 3 interactions
- **Full Test Configuration: 11 API Calls** — 1 campaign + 10 interactions

## Test File Comparison
| Test | API Calls | Unique Purpose |
|------|-----------|----------------|
| test_sariel_single_campaign_full.py | 21 | Comprehensive entity validation |
| test_sariel_with_prompts.py | 11 | Prompt debugging with logging |
| test_sariel_production_validation.py | 8 | Field-level validation with 3 AI personas |
| test_sariel_full_validation.py | 110 | 10 full replays for consistency |
| test_sariel_exact_production.py | ~15-20 | Production flow with auto-choice |
| test_sariel_consolidated.py | 4-11 | Unified test replacing 3 redundant files |

## Redundancy Findings
- **3 files can be removed** — single_campaign_full, with_prompts, production_validation
- **3 files to keep** — consolidated, full_validation, exact_production

## Recommendations
1. Remove three redundant tests (73-95% API call reduction achieved)
2. Consider adding recursive field counting to consolidated test
3. Update documentation to clarify test selection criteria

## Connections
- [[SarielTestSuiteConsolidation]] — prior consolidation work
- [[SarielCampaignReplayDesyncMeasurement]] — entity tracking context
- [[IntegrationTestsWithRealAPICalls]] — real API testing patterns
