---
title: "test_sariel_consolidated.py"
type: entity
tags: [test-file, consolidated, main-test]
sources: [sariel-test-files-analysis, sariel-test-suite-consolidation]
last_updated: 2026-04-08
---

## Description
Main consolidated test file replacing 3 redundant tests. Configurable via environment variables for different use cases.

## Configuration
- SARIEL_DEBUG_PROMPTS=true — enables prompt logging
- SARIEL_FULL_TEST=true — runs 10 interactions (default: 3)
- SARIEL_REPLAYS=N — number of campaign runs (default: 1)

## API Calls
- Default: 4 (1 campaign + 3 interactions)
- Full test: 11 (1 campaign + 10 interactions)
- With replays: N × calls per run

## Key Features
- Combines functionality from single_campaign, with_prompts, production_validation
- Configurable via environment variables
- Entity validation
- Game state field counting
- Optional prompt debugging
- Results saved to JSON in debug mode

## Connections
- [[SarielTestSuiteConsolidation]] — prior consolidation
- [[SarielTestFilesAnalysis]] — this analysis
