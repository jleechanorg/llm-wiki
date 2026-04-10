---
title: "Fantasy Calendar"
type: concept
tags: [datetime, calendar, fantasy, game-world]
sources: ["world-time-module-tests"]
last_updated: 2026-04-08
---

## Definition
A fantasy calendar system that supports dates invalid in Gregorian (e.g., February 30, month 13) for world-building in fictional settings.

## Key Properties
- **Month range**: Supports months beyond 12 (tested up to month 13)
- **Day flexibility**: Supports days like Feb 30 that are invalid in real-world calendars
- **Hours calculation**: calculate_hours_elapsed handles fantasy dates without raising ValueError
- **30-day months**: Uses 30-day month arithmetic for consistent calculations

## Test Coverage
- test_calculate_hours_elapsed_fantasy_date: Validates Feb 30 -> Mar 1 calculation returns 24 hours
- test_calculate_hours_elapsed_invalid_month_returns_none: Returns None for month=13 (truly invalid)

## Related Concepts
- [[WorldTime]] — supports fantasy calendar dates in game state
- [[TimeConsolidation]] — unified temporal representation
