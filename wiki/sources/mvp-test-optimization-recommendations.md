---
title: "MVP Test Optimization Recommendations"
type: source
tags: [testing, optimization, test-reducing, tdd, e2e, coverage]
source_file: "raw/mvp-test-optimization-recommendations.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Analysis of the test suite's size and structure, recommending ~4,054 lines (~8%) reduction across 5 categories. Phase 1 already removed 1,804 lines (10 files). Remaining recommendations target ~2,250 more lines through trimming overlapping tests, consolidating similar test groups, and splitting overly large files.

## Key Claims
- **Original test count**: 196 files (177 unit + 13 e2e + 6 integration/misc)
- **Current test count**: 186 files (after Phase 1 deletions)
- **Lines removed**: 1,804 lines from 10 deleted red-green bug fix tests
- **Total recommended reduction**: ~4,054 lines (~8% of total)
- **Remaining reduction target**: ~2,250 lines

## Categories

### Category 1: DELETE - Red-Green Bug Fix Tests (✅ COMPLETED)
Ten TDD test files created to verify bug fixes, now redundant with end-to-end tests. All deleted.

### Category 2: TRIM - Tests with e2e Overlap (~650 lines savings)
Trim unit tests that partially overlap e2e tests:
- God mode tests: 193 lines savings
- Entity tracking tests: 180 lines savings
- MCP tests: 274 lines savings

### Category 3: CONSOLIDATE - Overlapping Test Groups (~1,600 lines savings)
- Narrative response tests: 5 files → 2 files (~900 lines saved)
- JSON handling tests: 4 files → 2 files (~700 lines saved)

### Category 4: SPLIT - Overly Large Tests (maintainability)
Split files over 350 lines for parallel execution and maintainability:
- test_game_state.py (2,098 lines)
- test_world_logic.py (1,376 lines)
- test_v1_vs_v2_campaign_comparison.py (1,081 lines)
- test_concurrency_integration.py (674 lines)
- test_entity_tracking.py (633 lines)

### Category 5: KEEP - Valid Unit Tests
Comprehensive unit tests that provide value beyond e2e coverage.

## End-to-End Tests Coverage (KEEP ALL)
E2E tests in `mvp_site/tests/test_end2end/` total 4,544 lines covering:
- Campaign creation, continuation, retrieval
- Debug mode, god mode settings
- MCP protocol and error handling
- Entity tracking, timeline logging

## Connections
- [[EndToEndTests]] — comprehensive integration coverage preserved
- [[RedGreenTesting]] — methodology for bug fix verification tests
- [[TestOptimization]] — systematic reduction of test redundancy
