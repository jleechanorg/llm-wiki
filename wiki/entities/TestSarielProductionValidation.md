---
title: "test_sariel_production_validation.py"
type: entity
tags: [test-file, field-validation, ai-personas]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Test file with detailed field-level validation and counts. Makes 8 API calls: 1 campaign + 3 interactions + 4 state checks. Runs only 3 interactions for faster results.

## Status
**MOSTLY REDUNDANT** — covered by consolidated test except recursive field counting feature

## Key Features
- Recursive field counting for each entity type
- Uses all 3 AI personas (narrative, mechanics, calibration)
- Uses all custom options for maximum tokens
- Detailed field count breakdown per entity
- Focuses on state evolution tracking

## Connections
- [[TestSarielConsolidated]] — replacement test
- [[SarielTestFilesAnalysis]] — source analysis
