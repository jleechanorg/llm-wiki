---
title: "ISO 8601 Parsing"
type: concept
tags: [datetime, parsing, iso-8601, timestamp, timezone]
sources: ["world-time-module-tests"]
last_updated: 2026-04-08
---

## Definition
ISO 8601 parsing converts timestamp strings like "2025-03-15T10:45:30.123456Z" into structured datetime objects.

## Properties in World Time Context
- **Format**: YYYY-MM-DDTHH:MM:SS.ffffffZ (microsecond precision, optional Z for UTC)
- **Timezone handling**: Missing timezone defaults to UTC
- **Microseconds**: Preserved as separate field in world_time structure
- **Z suffix**: Indicates UTC timezone

## Related Concepts
- [[WorldTime]] — uses ISO 8601 parsing for LLM-generated timestamps
- [[TemporalCorrection]] — compares parsed timestamps for consistency
