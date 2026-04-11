---
title: "World Time Module Tests"
type: source
tags: [testing, world-time, datetime, timezone, python]
source_file: "raw/world-time-module-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating world_time module functions including parse_timestamp_to_world_time, extract_world_time_from_response, apply_timestamp_to_world_time, and world_time_to_comparable. Tests cover ISO 8601 timestamp parsing, timezone conversion, and month abbreviation handling.

## Key Claims
- **Timestamp parsing**: Parses ISO 8601 timestamps like "2025-03-15T10:45:30.123456Z" into structured world_time objects with year, month, day, hour, minute, second, and microsecond fields
- **Response extraction**: Extracts world_time from response objects containing timestamp_iso fields with timezone-aware conversion (e.g., +02:00 converts to UTC)
- **State application**: Applies timestamp strings to world_data state, populating missing world_time fields
- **Month abbreviations**: Handles abbreviated month names like "May" in world_time objects via world_time_to_comparable function

## Key Test Cases
- test_parse_timestamp_string_to_world_time:
  - Input: "2025-03-15T10:45:30.123456Z"
  - Expected output: {year: 2025, month: 3, day: 15, hour: 10, minute: 45, second: 30, microsecond: 123456}
- test_extract_world_time_from_timestamp_only_response:
  - Input: response with timestamp_iso "2026-12-01T08:00:00+02:00"
  - Expected: {year: 2026, month: 12, day: 1, hour: 6, minute: 0} (UTC conversion from +02:00)
- test_apply_timestamp_populates_missing_world_time:
  - Input: state_changes with timestamp "2027-07-04T21:05:45"
  - Expected: world_time object with full date/time fields
- test_world_time_to_comparable_accepts_may_abbreviation:
  - Input: world_time_dict with month: "May"
  - Expected: comparable tuple with month converted to integer 5

## Connections
- [[WorldTimeModule]] — the module under test
- [[ISO8601]] — timestamp format standard
- [[TimezoneConversion]] — timezone handling in timestamp extraction

## Contradictions
- None identified
