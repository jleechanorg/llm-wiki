---
title: "Sariel Test Suite Consolidation"
type: source
tags: [testing, optimization, api-costs, sariel, test-consolidation]
source_file: "raw/sariel-test-suite-consolidation.md"
sources: []
last_updated: 2026-04-08
---

## Summary
The Sariel test suite was consolidated from 7 redundant test files into 3 focused tests to reduce API calls and improve maintainability. This consolidation achieves 73-95% reduction in API calls for typical test runs.

## Consolidated Tests

### 1. `test_sariel_consolidated.py` (Main Test)
Replaces: `test_sariel_single_campaign_full.py`, `test_sariel_with_prompts.py`, `test_sariel_production_validation.py`

**Features**:
- Configurable via environment variables
- Comprehensive entity tracking validation
- Game state field counting
- Detailed results export in debug mode

**Environment Variables**:
| Variable | Purpose | Default |
|----------|---------|---------|
| SARIEL_DEBUG_PROMPTS | Enable prompt logging | false |
| SARIEL_FULL_TEST | Run 10 interactions | 3 |
| SARIEL_REPLAYS | Run multiple campaigns | 1 |

### 2. `test_sariel_production_methods.py`
Tests `get_initial_story` and `continue_story` methods directly with minimal API calls (2-3 total).

### 3. `test_sariel_entity_debug.py`
Specialized debugging for entity disappearance issues with prompt interception.

## API Call Reduction

| Test Mode | Before | After | Savings |
|-----------|--------|-------|---------|
| Regular | 11-60 calls | 3 calls | 73-95% |
| Full | 60+ calls | 10 calls | 83% |
| Debug | 22+ calls | 2-10 calls | 55-91% |

## Benefits
- Reduced API costs
- Faster test execution
- Better maintainability
- Configurable test depth
- Clear, non-overlapping test purposes
