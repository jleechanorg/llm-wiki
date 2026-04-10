---
title: "test_sariel_single_campaign_full.py"
type: entity
tags: [test-file, api-calls, entity-validation]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Test file running one Sariel campaign with first 10 interactions, validating all entities and game state. Makes 21 API calls total: 1 campaign creation + 10 interactions + 10 state checks.

## Status
**REDUNDANT** — fully covered by test_sariel_consolidated.py with SARIEL_FULL_TEST=true

## Key Features
- Comprehensive entity tracking validation
- Detailed game state field validation (player, NPC, world, combat)
- Cassian problem specific tracking
- Per-interaction detailed results

## Connections
- [[TestSarielConsolidated]] — replacement test
- [[SarielTestFilesAnalysis]] — source analysis
