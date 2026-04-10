---
title: "Evidence Preservation"
type: concept
tags: [testing, debugging, cross-process]
sources: [conflict-resolution-pr-3902]
last_updated: 2026-04-08
---

## Description
Strategy for capturing and saving diagnostic evidence (logs, process state, server data) during test execution, especially for cross-process tests that involve server restarts.

## In This Resolution
Evidence preservation was prioritized in the merge:
- Retained PR's intent classification metadata additions
- Kept main's pre-restart evidence saving (ps, lsof, server logs)
- Discarded PR's template overwrite that would have clobbered evidence logic

## Key Evidence Types
- Process state (`ps` output)
- File descriptors (`lsof` output)
- Server logs
- Intent classification metadata (intent, classifier_source, confidence, routing_priority)

## Related Concepts
- [[CrossProcessTesting]] — Testing pattern requiring evidence preservation
- [[IntentClassification]] — Metadata being captured
- [[MergeConflictResolution]] — Where evidence priorities were decided
