---
title: "test_sariel_full_validation.py"
type: entity
tags: [test-file, multi-run, consistency]
sources: [sariel-test-files-analysis]
last_updated: 2026-04-08
---

## Description
Test file running 10 full campaign replays with complete validation. Makes 110 API calls: 10 campaigns × 11 calls each.

## Status
**KEEP** — unique multi-run validation capability

## Key Features
- Multiple full campaign runs for consistency testing
- Comprehensive validation errors tracking
- Per-run and overall statistics
- Cassian problem success rate across runs

## Connections
- [[SarielTestFilesAnalysis]] — source analysis
- [[SarielCampaignReplayDesyncMeasurement]] — desync measurement context
