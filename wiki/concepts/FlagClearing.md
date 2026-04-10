---
title: "Flag Clearing"
type: concept
tags: [state-management, modal-agent]
sources: ["modal-state-lifecycle-tests", "modal-state-management-integration-tests"]
last_updated: 2026-04-08
---

## Summary
Mechanism for clearing stale flags when new modals become available or when exiting a modal. Ensures old state doesn't block future activations.

## Key Claims
- **Removal, not False**: Stale flags should be removed from dict, not set to False
- **New modal availability**: Clearing flags when new level-up becomes available
- **Exit clearing**: Exiting one modal clears flags that could cause recapture
- **Cross-modal defense**: Level-up exit clears character_creation_in_progress

## Connections
- [[Modal State Management]] — applies to all modals
- [[State Transitions]] — lifecycle transitions involve clearing
- [[Integration Tests for Modal State Management]] — validates clearing behavior
