---
title: "PlanningBlock Choices Canonical List Format (PR #4534)"
type: source
tags: [python, testing, planning-block, choices, schema-validation, canonicalization]
source_file: "raw/test_planning_block_choices_canonical.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating that `PlanningBlock.choices` is canonicalized to a list format (`list[PlanningChoice]`), converting from dict format and handling duplicate IDs with deterministic suffixes.

## Key Claims
- **Schema validation accepts list format**: Native list input passes validation with correct `id` field extraction
- **Dict-to-list conversion**: Schema automatically converts dict-keyed choices to list format with auto-generated IDs
- **Duplicate ID handling**: Duplicate IDs get deterministic suffixes (`attack` → `attack`, `attack_1`, `attack_2`)
- **JSON string normalization**: Helper function handles JSON string input, converting to validated list

## Key Quotes
> "Planning choices are canonicalized to list[PlanningChoice]." — test class docstring

## Connections
- [[PlanningBlock]] — technical concept being validated
- [[NarrativeResponse]] — schema class containing planning_block field
- [[normalize_planning_block_choices]] — helper function under test

## Contradictions
- None identified — this validates new functionality, not existing behavior
