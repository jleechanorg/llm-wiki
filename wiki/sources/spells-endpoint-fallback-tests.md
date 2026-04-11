---
title: "Spells Endpoint Fallback Message Tests"
type: source
tags: [tdd, unit-testing, api-endpoint, python, flask, firestore]
source_file: "raw/spells-endpoint-fallback-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the `/api/campaigns/<id>/spells` endpoint validating the fallback message path (lines 2568-2574 in main.py). When spell_slots are present but spells_known, cantrips, and spells_prepared are all empty, the summary must prompt the user to set up their spell list.

## Key Claims
- **Fallback Message Required**: When spell slots exist but no spell list is recorded, the endpoint must return: 'No spell list recorded. Type: "What spells do I know?" to set them up.'
- **Multiple Formats Supported**: Fallback triggers for both direct spell_slots format and resources.spell_slots format
- **No False Positives**: Fallback must NOT appear when spells_known, cantrips, or spells_prepared are populated, or when no spell slots exist at all

## Key Test Functions
- `test_fallback_message_shown_when_slots_present_but_no_spells`: Validates fallback with direct spell_slots format
- `test_fallback_shown_with_resources_spell_slots_format`: Validates fallback with resources.spell_slots format
- `test_no_fallback_when_spells_known_present`: Ensures no fallback when spells_known is populated
- `test_no_fallback_when_cantrips_present`: Ensures no fallback when cantrips exist
- `test_no_fallback_when_no_spell_slots_at_all`: Ensures no fallback for non-spellcasters

## Connections
- [[settings-page-api-tests-mcp-architecture]] — related API endpoint tests
- [[functional-validation-test-runner]] — broader UI testing

## Contradictions
- None identified
