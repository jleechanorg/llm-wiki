---
title: "JSON Parsing"
type: concept
tags: [json, parsing, python]
sources: [state-update-integration-tests]
last_updated: 2026-04-08
---

## Description
The process of extracting structured data from JSON responses rather than parsing markdown blocks or narrative text.

## Why It Matters
Previous implementation used markdown blocks like [STATE_UPDATES_PROPOSED] which could leak into narrative. JSON parsing provides cleaner separation.

## Implementation
- Use structured_response from LLMResponse
- Property `state_updates` extracts from structured_response
- JSON mode takes precedence over markdown blocks

## Connections
- [[StateUpdates]] — the data being parsed
- [[ParseStructuredResponse]] — the function that performs parsing
- [[StateUpdateIntegrationTests]] — tests this concept
