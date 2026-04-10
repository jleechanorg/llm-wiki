---
title: "test_sariel_exact_production.py"
type: entity
tags: [test-file, production-flow, auto-choice]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Test file using exact production campaign example, always picks choice 1. Makes ~15-20 API calls depending on exact data.

## Status
**KEEP** — unique production flow with auto-choice selection

## Key Features
- Uses exact production prompts from JSON
- Auto-continues with choice 1 strategy
- Recursive field counting
- Checks for STATE_UPDATES_PROPOSED in narrative
- Extracts choice options from narrative

## Connections
- [[SarielExactProductionCampaignExample]] — production example source
- [[SarielTestFilesAnalysis]] — source analysis
