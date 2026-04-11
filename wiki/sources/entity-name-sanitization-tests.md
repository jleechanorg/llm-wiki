---
title: "Entity Name Sanitization Tests"
type: source
tags: [python, testing, string-processing, sanitization, unicode]
source_file: "raw/test_entity_name_sanitization.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the `sanitize_entity_name_for_id` function in `llm_service.py`. Tests cover entity name transformation for safe use as IDs: apostrophe handling, special character removal, unicode/accent processing, whitespace normalization, and edge cases.

## Key Claims
- **Apostrophe handling**: Multiple apostrophes collapsed (e.g., "Ma'at's" → "maats")
- **Special character substitution**: @, #, $, %, &, *, !, ? converted to underscores or removed
- **Unicode handling**: Latin accents preserved (é→e, ï→i), Cyrillic/Japanese/emoji removed entirely
- **Whitespace normalization**: Leading/trailing/multiple spaces collapsed to single underscore
- **Consecutive special chars**: Multiple special characters collapse to single underscore

## Key Test Cases
| Test | Scenario | Expected |
|------|----------|----------|
| Basic sanitization | "Cazador's Spawn" | "cazadors_spawn" |
| Unicode | "Café" | "caf" |
| Special chars | "Name@Email.com" | "name_email_com" |
| Edge case | Empty string | "" |

## Connections
- [[LlMService]] — module containing this function
- [[EntityNameSanitization]] — concept of transforming names to valid IDs
