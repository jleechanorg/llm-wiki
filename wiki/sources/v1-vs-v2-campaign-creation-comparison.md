---
title: "V1 vs V2 Campaign Creation Comparison Test"
type: source
tags: [testing, e2e, v1-v2-comparison, playwright, tdd, qa-protocol]
source_file: "raw/v1_vs_v2_campaign_comparison_test.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Systematic E2E comparison test following TDD methodology to compare V1 (Flask on port 8081) vs V2 (React on port 3002) campaign creation workflows. Tests cover three campaign types: Dragon Knight default, Custom with Lady Elara, and Full Custom.

## Key Claims
- **Test Matrix Coverage**: 3 campaign types × 2 system versions × 7 test scenarios = systematic coverage
- **V1 vs V2 Parity**: Validates equivalent functionality between Flask backend and React frontend
- **Evidence Documentation**: Screenshots, API timing, console logs, error states captured per QA protocol
- **E2E Validation**: Uses Playwright for browser automation testing complete user flows
- **Red/Green Phases**: TDD methodology with failure verification before success verification

## Test Coverage
- `TestMatrix.get_test_matrix()`: Generates all test combinations
- `EvidenceCollector`: Captures screenshots, API logs, console logs, performance data
- Campaign types: Dragon Knight default, Custom with Lady Elara, Full Custom
- Scenarios: navigation_flow, form_interaction, api_integration, planning_block_functionality (V2), character_selection, gameplay_transition, error_handling

## Connections
- [[Playwright]] — Browser automation framework used for E2E testing
- [[TDD]] — Test-Driven Development methodology followed
- [[Flask]] — V1 backend framework (port 8081)
- [[React]] — V2 frontend framework (port 3002)
- [[Campaign Creation]] — Core workflow being tested

## Contradictions
- None identified
