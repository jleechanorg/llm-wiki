---
title: "Story Context Tests - Consolidated"
type: source
tags: [tdd, unit-testing, python, context-compaction, firestore]
source_file: "raw/story-context-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Consolidated tests for story_context handling in context_compaction.py covering type safety guards against malformed Firestore data (Bug worktree_logs6-txx) and warning logic that only emits warnings when reduction > 0. Test matrix coverage: [2,1,1] through [2,2,3] (8 type safety tests + 2 warning logic tests).

## Key Claims
- **Type Safety Guards**: Defensive guards against non-dict story_context entries prevent AttributeError crashes when Firestore returns malformed data
- **Warning Logic**: Warnings only emitted when actual token reduction occurs (reduction > 0), avoiding noise from no-op scenarios
- **Mixed Valid/Invalid Processing**: Mixed valid dict entries and invalid non-dicts should skip invalid entries and process valid ones
- **All Invalid Handling**: All invalid entries should return empty story_text without crashing
- **Empty List Handling**: Empty story_context list should return empty string without errors

## Key Quotes
> "test_all_valid_dicts_processes_normally" — baseline ensures normal operation isn't broken by type safety guards
> "test_mixed_valid_invalid_skips_invalid_entries" — currently FAILS with AttributeError on "string".get("text", "")

## Connections
- [[ContextCompaction]] — module being tested for budget allocation
- [[TypeSafetyGuards]] — defensive programming pattern for handling malformed data
- [[FirestoreDataHandling]] — data validation for NoSQL database responses

## Contradictions
- None identified
