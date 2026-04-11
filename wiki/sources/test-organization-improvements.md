---
title: "Test Organization Improvements"
type: source
tags: [testing, test-maintenance, mvp-site, entity-tracking, constants, integration-testing]
source_file: "raw/test-organization-improvements.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Project to fix failing tests in the mvp_site/tests directory by updating them to reflect the current codebase architecture and removing references to archived features. All test failures were identified as test maintenance debt, not actual bugs in production code.

## Key Claims
- **9 failing tests analyzed** — all failures traced to outdated test expectations, not production bugs
- **4 test files fixed** — updated to match current single-system architecture
- **15 tests now passing** — test_constants.py fully operational
- **3 tests moved to integration/** — require google-genai module

## Root Cause Analysis

### Archived Constants Referenced
- Calibration system — removed from codebase
- Destiny system — removed from codebase  
- PROMPT_TYPE_ENTITY_SCHEMA — integrated into game_state
- PROMPT_TYPE_CALIBRATION — archived feature

### Architecture Evolution
- **Old**: Dual-system (Narrative Flair + Calibration Rigor)
- **New**: Single-system with entity tracking integrated into game_state

## Test Fixes Applied

### Fixed Tests (now passing)
- test_constants.py — 15 tests pass
- test_entity_tracking.py — 8 tests pass
- test_firestore_helpers.py — 15 tests pass (fixed logging assertion)
- test_think_block_protocol.py — 19 tests pass (updated to match current prompts)

### Moved to test_integration/
- test_pr_state_sync_entity.py — requires google-genai
- test_function_validation_flow.py — requires google-genai
- test_refactoring_helpers.py — requires google-genai

## Connections
- [[EntityTracking]] — core feature being tested
- [[GameStateIntegration]] — where entity tracking now lives
- [[IntegrationTesting]] — test category for google-genai dependent tests

## Contradictions
- None identified
