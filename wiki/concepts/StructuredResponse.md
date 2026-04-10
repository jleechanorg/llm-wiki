---
title: "Structured Response"
type: concept
tags: [api, schema, response]
sources: [state-update-integration-tests]
last_updated: 2026-04-08
---

## Description
A schema-defined response format from the LLM that includes both narrative text and structured data (state_updates, entities_mentioned, location_confirmed).

## Contrast with Markdown Blocks
- **Structured Response**: JSON with defined schema, type-safe
- **Markdown Blocks**: Text markers like [STATE_UPDATES_PROPOSED], prone to leakage

## Benefits
- Type safety via Pydantic
- Clear separation of narrative vs state
- No leakage into story output

## Connections
- [[NarrativeResponse]] — the schema
- [[JSONParsing]] — how to extract from it
- [[LLMResponse]] — wraps it
