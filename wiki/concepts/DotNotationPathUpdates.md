---
title: "Dot-Notation Path Updates"
type: concept
tags: [firestore, data-updates, nested-structures, path-syntax]
sources: []
last_updated: 2026-04-08
---

## Description
A data update pattern where dot-separated keys are expanded into nested dictionary structures. For example, `"a.b.c": value` becomes `{a: {b: {c: value}}}`.

## Use Case
When updating deeply nested fields in NoSQL databases like Firestore, dot-notation allows concise path specification without explicitly constructing the full nested structure.

## Implementation Notes
- Must handle path segments that don't yet exist (create them)
- Must merge with existing nested structures (not overwrite siblings)
- Common bug: literal key creation instead of nested expansion

## Related
- [[UpdateCampaign]] — function implementing this pattern
- [[FirestoreService]] — module containing the implementation
