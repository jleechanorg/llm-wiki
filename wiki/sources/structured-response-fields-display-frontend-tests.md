---
title: "Structured Response Fields Display Frontend Tests"
type: source
tags: [testing, javascript, frontend, structured-data, ui]
source_file: "raw/structured-response-fields-display-frontend-tests.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the complete data flow from API response to UI rendering for structured response fields. Tests verify that debug_info contains nested dice_rolls and resources, and that appendToStory accepts fullData parameter for frontend display.

## Key Claims
- **FullData Parameter**: appendToStory function must accept fullData parameter containing full API response
- **Nested Debug Info**: dice_rolls and resources are nested inside debug_info, not at top level
- **Debug Mode Fields**: entities_mentioned, location_confirmed, and state_updates exist at response top level
- **Schema Compliance**: Response structure matches game_state_instruction.md schema

## Key Quotes
> "assert.ok(fullData.debug_info, 'fullData should contain debug_info')"

## Connections
- [[GameStateInstruction]] — defines the schema these tests validate against
- [[StructuredFieldsUtils]] — backend extraction utilities
- [[DebugInfoDisplay]] — frontend component for rendering debug information

## Contradictions
[]
