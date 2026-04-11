---
title: "Schema Strictness and Schema-Coverage Guard Tests"
type: source
tags: [schema, json-schema, testing, coverage, validation, guard-rails]
source_file: "raw/test_schema_strictness_coverage.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Tests validating JSON schema structure for routing state objects and verifying code paths exercise schema-defined fields. The test suite ensures EncounterState, RewardsPending, CustomCampaignState, and CombatState have explicit properties, and validates the check_schema_coverage.py script reports no missing routing paths.

## Key Claims
- **Routing Objects Have Explicit Properties**: EncounterState, RewardsPending, CustomCampaignState, and CombatState each define required properties like encounter_completed, rewards_processed, level_up_pending
- **Schema Coverage Script Validates Paths**: check_schema_coverage.py verifies code exercises schema-defined fields and reports missing paths
- **Top-Level State Uses Structured Refs**: GameState references structured types via $ref rather than inline definitions
- **Canonical Equipment Slots Include Prompt Slots**: Character.equipped_items includes shoulders, chest, waist, legs from prompt generation

## Key Quotes
> "test_schema_coverage_script_reports_no_missing_routing_paths" — validates all routing state paths are exercised in code

## Connections
- [[GameStateSchema]] — defines the JSON schema being tested
- [[CheckSchemaCoverage]] — script that validates schema coverage
- [[SchemaStrictness]] — enforces schema has explicit property definitions

## Contradictions
- None detected
