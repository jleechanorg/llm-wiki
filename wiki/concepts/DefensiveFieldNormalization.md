---
title: "Defensive Field Normalization"
type: concept
tags: [schema, defensive-programming, type-safety]
sources: []
last_updated: 2026-01-18
---

## Definition

Defensive Field Normalization is a pattern where the server defensively normalizes data at state boundaries rather than relying on schema validation alone. When an expected string field receives a dict, or a required field is missing, the server normalizes it to a safe default and logs the discrepancy — rather than crashing or returning null.

## Problem

Two distinct concepts can share the same field name (e.g., `game_state['location']`):
1. **LLM output field**: string narrative description of current location
2. **Entity tracking field**: persistent state for entity tracking

When entity tracking reads `game_state.get('location', 'Unknown Location')` and the LLM has set it as a dict `{'description': '...'}`, the Pydantic validator crashes: "Input should be a valid string."

## Solution Pattern

```python
# Defensive normalization at state boundary
location = state.get("location", "Unknown Location")
if isinstance(location, dict):
    location = location.get("description", location.get("display_name", "Unknown Location"))
elif not isinstance(location, str):
    location = "Unknown Location"
```

## Defense in Depth Layers

1. **LLM instructions**: Document expected field format explicitly
2. **Schema validation**: Fail fast on wrong types (Pydantic)
3. **Defensive normalization**: Safe fallback at state boundary (this pattern)
4. **Error handling**: Never return null/none — always a safe default

## Sources

- fix-location-field-fragility.json: entity tracking crashes on dict location field
