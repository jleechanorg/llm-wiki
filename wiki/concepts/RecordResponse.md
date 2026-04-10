---
title: "Record Response"
type: concept
tags: [testing, capture, data-recording]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Method for capturing response data after an interaction completes. Records response payload, calculates duration, and updates interaction status.

## Parameters
- `interaction_id` — UUID from capture_interaction
- `response` — dict of response data

## Behavior
- Stores response in interaction record
- Calculates duration_ms from start time
- Marks status as "success"

## Related
- [[CaptureInteraction]] — pair for complete recording
- [[ErrorTracking]] — failure case handling
