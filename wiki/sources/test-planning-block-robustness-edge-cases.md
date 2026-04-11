---
title: "Test Planning Block Robustness and Edge Case Handling"
type: source
tags: [python, testing, planning-block, edge-cases, robustness, json, validation]
source_file: "raw/test_planning_block_robustness.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating the robustness of JSON-only planning block format in NarrativeResponse. Tests cover null handling, string rejection, type validation, and extreme input scenarios. The tests enforce that string-format planning blocks are no longer supported.

## Key Claims
- **Null planning block preserved**: None input converts to empty dict, not AttributeError
- **String format rejected**: Empty, whitespace, and JSON-like string formats are rejected with ERROR logs
- **Type validation enforced**: Integer and list planning blocks are rejected as INVALID PLANNING BLOCK TYPE
- **Dict format accepted**: Valid dict with thinking/choices keys is properly preserved
- **Extreme input handling**: Planning blocks with 100+ choices are handled without performance degradation

## Key Quotes
> "STRING PLANNING BLOCKS NO LONGER SUPPORTED" — enforced error message for all string inputs

> "INVALID PLANNING BLOCK TYPE" — enforced error message for non-dict/non-null inputs

## Connections
- [[PlanningBlock Choices Canonical List Format]] — validates canonical list schema
- [[Frontend JSON Planning Block Processing Tests]] — frontend validation of JSON format
- [[Test Planning Block Robustness and Edge Case Handling]] — this page

## Contradictions
- None identified — validates new JSON-only format that supersedes string format
