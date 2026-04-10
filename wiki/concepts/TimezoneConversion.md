---
title: "Timezone Conversion"
type: concept
tags: [datetime, timezone, conversion]
sources: [world-time-module-tests]
last_updated: 2026-04-08
---

## Definition
Timezone conversion is the process of translating timestamps from one timezone representation to another, typically converting local time to UTC for consistent storage and comparison.

## Relevance
The world_time module converts timestamps with explicit timezone offsets (e.g., +02:00) to UTC by subtracting the offset hours.

## Example
"2026-12-01T08:00:00+02:00" converts to "2026-12-01T06:00:00Z" (08:00 - 02:00 = 06:00 UTC)

## Connected Entities
- [[ISO8601]] — format that includes timezone information
- [[WorldTimeModule]] — performs timezone conversion
