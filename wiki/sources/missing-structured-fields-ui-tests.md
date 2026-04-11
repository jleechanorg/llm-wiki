---
title: "Missing Structured Fields UI Tests"
type: source
tags: [javascript, testing, ui, structured-data, frontend]
source_file: "raw/test_missing_structured_fields_ui.js"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript unit tests validating the UI display of three missing structured fields: god_mode_response, entities_mentioned, and location_confirmed. Tests verify HTML generation for each field type matches expected schema structure.

## Key Claims
- **God Mode Response**: Should display prominently with emoji 🔮 and use `<pre>` tag for formatting
- **Entities Mentioned**: Should render as unordered list with 👥 emoji, displaying each entity as list item
- **Location Confirmed**: Should always display when present (not "Unknown") with 📍 emoji
- **Combined Display**: All three fields can render together in a single response

## Key Quotes
> "generateStructuredFieldsHTML(fullData, debugMode)" — function signature for structured field rendering

## Connections
- Related to [[Main.py Structured Response Building]] — server-side schema
- Related to [[LLMResponse Structured Fields Parsing]] — field extraction from LLM responses
- Related to [[MCP Interaction Structured Fields]] — API gateway field handling

## Contradictions
- None detected
