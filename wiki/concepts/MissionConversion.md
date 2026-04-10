---
title: "Mission Conversion"
type: concept
tags: [state-migration, data-transformation]
sources: ["mission-conversion-helpers-tests", "mission-auto-completion-e2e-tests"]
last_updated: 2026-04-08
---

## Description
Process of converting dict-style mission storage to list format. Automatically generates mission_id from dict key, updates existing missions by matching mission_id, and validates mission data before conversion.

## Key Methods
- Auto-generates mission_id from dict key (e.g., "quest_1" becomes mission_id="quest_1")
- Updates existing missions instead of duplicating when mission_id matches
- Skips invalid data (non-dict values) with warning logs

## Related Pages
- [[Mission Conversion Helpers Tests]] — unit tests for conversion logic
- [[Mission Auto-Completion E2E Tests]] — E2E tests for completed_missions field migration
