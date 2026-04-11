---
title: "World Time Module"
type: source
tags: [python, datetime, calendar, world-building, temporal]
source_file: raw/world_time_module.py
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing world time handling utilities for the World of Assiah campaign. Supports multiple calendar systems (Forgotten Realms, Grayhawk, Gregorian) with month name normalization, timestamp parsing, and temporal comparison functions.

## Key Claims
- **Multi-Calendar Support**: Normalizes months from Forgotten Realms, Grayhawk, and Gregorian calendars to 1-12 for temporal comparison
- **Month Name Mapping**: 36 month aliases mapped (full names and abbreviations) allowing flexible input parsing
- **Timestamp Normalization**: Converts ISO timestamps with timezone offsets to UTC for consistent temporal comparisons
- **LLM State Integration**: Extracts world_time from LLM response state_updates with fallback to timestamp_iso fields
- **Safe Type Handling**: Uses `_safe_int` helper for graceful handling of malformed numeric values

## Key Functions
- `world_time_to_comparable`: Converts world_time dict to tuple for temporal comparison
- `parse_timestamp_to_world_time`: Parses ISO-like timestamps to world_time dict
- `extract_world_time_from_response`: Extracts world_time from LLM response state_updates
- `_has_required_date_fields`: Validates presence of year, month, day in world_time

## Connections
- [[World of Assiah]] — temporal system for the campaign setting
- [[World Time Module Tests]] — validates these functions with TDD
