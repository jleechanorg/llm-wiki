---
title: "Firestore Structured Fields Handling Tests"
type: source
tags: [python, testing, firestore, structured-fields, unit-tests]
source_file: "raw/test_firestore_structured_fields.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating that `add_story_entry` in firestore_service.py properly stores and retrieves structured fields in Firestore. Tests cover three scenarios: full structured fields, no structured fields, and partial structured fields.

## Key Claims
- **add_story_entry stores structured fields correctly**: When structured_fields dict is provided, fields like session_header, planning_block, dice_rolls, resources, and debug_info are stored in the Firestore document
- **Structured fields are optional**: The function works without structured fields, storing only basic fields (text, actor, timestamp, part)
- **Partial structured fields work**: Only providing some structured fields results in only those fields being stored
- **Constants define field names**: The mvp_site.constants module defines FIELD_SESSION_HEADER, FIELD_PLANNING_BLOCK, FIELD_DICE_ROLLS, FIELD_RESOURCES, FIELD_DEBUG_INFO

## Key Quotes
> "Test add_story_entry properly stores structured fields" — test method documentation

## Connections
- [[Firestore]] — the database service being tested
- [[StructuredFields]] — the pattern being validated
- [[UnitTesting]] — the testing methodology used

## Contradictions
None detected.
