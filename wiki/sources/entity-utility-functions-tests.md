---
title: "Entity Utility Functions Tests"
type: source
tags: [python, testing, entity-utils, filtering]
source_file: "raw/test_entity_utility_functions.py"
last_updated: 2026-04-08
---

## Summary
Unit tests for entity utility functions that filter unknown entities from lists. Tests validate case-insensitive filtering of "Unknown" values while preserving list order.

## Key Claims
- **filter_unknown_entities**: Removes all variants of "Unknown" (case-insensitive) from entity lists while preserving original order
- **is_unknown_entity**: Detects unknown entities with case-insensitive matching
- **Order Preservation**: Filtering maintains the original ordering of known entities
- **Empty Handling**: Both functions handle empty lists without errors

## Key Test Cases
- `test_filter_unknown_entities_removes_unknown` - Basic filtering
- `test_filter_unknown_entities_case_insensitive` - Case-insensitive matching
- `test_is_unknown_entity_true_cases` - Detection of unknown variants
- `test_filter_unknown_entities_preserves_order` - Order preservation

## Connections
- [[EntityTracking]] — utility functions used in entity tracking pipeline
- [[FilterUnknownEntities]] — core function being tested
