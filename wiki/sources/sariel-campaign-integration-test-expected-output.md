---
title: "Sariel Campaign Integration Test - Expected Output"
type: source
tags: [testing, integration-test, sariel, entity-tracking, field-validation, expected-output]
source_file: "raw/sariel-campaign-integration-test-expected-output.md"
sources: [sariel-campaign-integration-test-execution, sariel-test-files-analysis, sariel-campaign-replay-desync-measurement]
last_updated: 2026-04-08
---

## Summary
Expected test output showing the complete run of the Sariel campaign integration test including field validation metrics, entity tracking results, and Cassian Problem handling verification.

## Key Claims
- **5834 Fields Validated** — across 10 interactions, averaging 583.4 fields per interaction
- **90% Entity Tracking Success Rate** — 9 of 10 interactions successful
- **Cassian Problem Handled** — edge case for player-referenced NPCs not in current scene successfully processed
- **Model: gemini-1.5-flash** — used for initial story generation

## Test Execution Flow
1. Campaign creation with 12 top-level fields (player character, world data, NPCs, combat state)
2. 10 interactions from initial setup through full replay
3. Entity tracking validation per interaction
4. State validation with field counts per NPC

## Key Metrics
| Metric | Value |
|--------|-------|
| Total Interactions | 10 |
| Successful Entity Tracking | 9/10 (90%) |
| Total Fields Validated | 5834 |
| Fields per Interaction | 583.4 average |
| Failed Interaction | Interaction 9 (Magister Kantos missing) |

## Connections
- [[SarielCampaignIntegrationTestExecution]] — actual test execution that produced similar output
- [[SarielTestFilesAnalysis]] — test file structure and API call patterns
- [[SarielCampaignReplayDesyncMeasurement]] — desync measurement methodology

## Contradictions
- None — this expected output aligns with documented entity tracking challenges showing 90% success vs the 50% measured in earlier desync analysis
