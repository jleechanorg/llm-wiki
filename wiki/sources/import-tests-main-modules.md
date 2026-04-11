---
title: "Import Tests for Main Modules"
type: source
tags: [python, testing, import, module-dependencies, firestore, llm-service]
source_file: "raw/test_imports.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating that all main application modules can be imported without errors. Tests verify the presence of key attributes in each module to ensure proper module structure and API consistency.

## Key Claims
- **firestore_service importable**: Module must have `add_story_entry` and `create_campaign` attributes
- **llm_service importable**: Module must have `continue_story` attribute
- **main importable**: Module must have `create_app` factory function
- **game_state importable**: Module must have `GameState` class
- **constants importable**: Module must have structured field constants (FIELD_SESSION_HEADER, FIELD_PLANNING_BLOCK, FIELD_DICE_ROLLS, FIELD_RESOURCES, FIELD_DEBUG_INFO)
- **structured_fields_utils importable**: Module must have `extract_structured_fields` function
- **narrative_response_schema importable**: Module must have `NarrativeResponse` schema
- **llm_response importable**: Module must have `LLMResponse` class

## Key Quotes


## Connections
- [[FirestoreService]] — tested module for database operations
- [[LLMService]] — tested module for AI/LLM interactions
- [[GameState]] — tested module for game state management
- [[Constants]] — tested module for application constants

## Contradictions
- []
