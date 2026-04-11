---
title: "Planning Block List Canonicalization Tests"
type: source
tags: [python, testing, planning-block, normalization, canonicalization, tdd]
source_file: "raw/test_planning_block_list_canonical.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating the `normalize_planning_block_choices` function in `campaign_upgrade` module. Tests cover dict-to-list conversion, canonical ID preservation, empty input handling, and deterministic duplicate ID suffixing.

## Key Claims
- **List input preserves IDs**: Canonical list input with explicit IDs passes through unchanged
- **Dict-to-list conversion**: Dict-keyed choices convert to list format using keys as IDs
- **Empty/whitespace ID fallback**: Empty or whitespace-only IDs fallback to slugified text
- **Duplicate ID handling**: Duplicate IDs get deterministic suffixes (e.g., "attack" → "attack", "attack_1")
- **Empty inputs**: None and empty dict inputs return empty choices list

## Key Quotes
> "normalize_planning_block_choices returns list-format choices." — test class docstring

## Connections
- [[campaign_upgrade]] — module containing the function under test
- [[normalize_planning_block_choices]] — function being validated
- [[PlanningBlock]] — the parent structure being normalized

## Contradictions
- None identified
