---
title: "Entity Injection"
type: concept
tags: [entity-tracking, injection, dual-pass, enhancement]
sources: [parallel-dual-pass-optimization]
last_updated: 2026-04-08
---

## Definition
The process in Pass 2 of the dual-pass verification system where missing entities are injected into the narrative to ensure entity tracking accuracy.

## Technical Details
- Triggered when `enhancement_needed` flag is true from Pass 1 validation
- Processes `missing_entities` list returned by entity validator
- Runs as background task in parallel with user reading initial response
- Results cached for future reference and replaced via `replaceStoryEntry()`

## Related Concepts
- [DualPassVerification](DualPassVerification.md) — the parent system
- [EntityTracking](EntityTracking.md) — the broader capability being maintained
- [GracefulDegradation](GracefulDegradation.md) — fallback handling if enhancement fails
