---
title: "ParseStructuredResponse"
type: concept
tags: [function, json-parsing, error-handling]
sources: ["main-user-scenario-fix-god-mode-json"]
last_updated: 2026-04-08
---

Function in `mvp_site.narrative_response_schema` that parses AI responses and extracts structured data. Handles both valid JSON with proper field extraction and malformed JSON by returning standardized error messages instead of raw JSON.

## Key Behavior
- Valid JSON: Extracts `narrative`, `god_mode_response`, `entities_mentioned`, `location_confirmed`, `state_updates`, `debug_info`
- Invalid JSON: Returns standardized "invalid json response" message, never exposes raw JSON keys

## Related Concepts
- [[NarrativeResponseSchema]] — the schema this function implements
- [[GodMode]] — game mode where this function handles god_mode_response field
