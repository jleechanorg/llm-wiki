---
title: "app.js Structured Fields Implementation Tests"
type: source
tags: [javascript, testing, nodejs, frontend, structured-fields, streaming]
source_file: "raw/app-js-structured-fields-implementation-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Node.js test file that validates the actual implementation of structured fields in app.js and streaming.js. Tests include fullData parameter handling, dice_rolls extraction, resources extraction, spicy mode choice routing, and streaming client fallback behavior.

## Key Claims
- **generateStructuredFieldsHTML**: Function exists in app.js for generating structured field HTML
- **fullData Parameter**: appendToStory accepts fullData parameter for accessing top-level data
- **Dice Rolls Extraction**: Code extracts dice_rolls from top-level fullData object
- **Resources Extraction**: Code extracts resources from top-level fullData object
- **Spicy Mode Routing**: Choice handlers detect enable_spicy_mode and disable_spicy_mode choices
- **Settings Endpoint**: Spicy choices route to /api/settings endpoint
- **Streaming Fallback**: StreamingClient falls back to regular interaction when unavailable
- **Auth Init Wait**: Streaming client waits for auth initialization before requesting headers
- **Auth Fallback**: Streaming client has fallback path for transient auth races

## Key Quotes
> "StreamingClient is unavailable; falling back to regular interaction flow." — fallback message

> "await handleRegularInteraction(userInput, mode);" — fallback handler call

## Connections
- [[frontend_v1/app.js]] — main frontend file being tested
- [[frontend_v1/js/streaming.js]] — streaming client implementation
- [[Spicy Mode]] — feature toggle tested
- [[StreamingClient]] — client with fallback behavior

## Contradictions
- []
