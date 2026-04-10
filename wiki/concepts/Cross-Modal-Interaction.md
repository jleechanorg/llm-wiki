---
title: "Cross-Modal Interaction"
type: concept
tags: [modal-agent, testing, state-management]
sources: ["modal-state-management-integration-tests"]
last_updated: 2026-04-08
---

## Definition
Testing the interactions and flag pollution between different modals (character creation, level-up, campaign upgrade) in the game system.

## Key Principles
- Exiting one modal should clear stale flags from other modals
- Multiple modal flags should not coexist - only one modal should be active
- Defensive cleanup of stale flags prevents recapture by other modal locks

## Related Tests
- [[Modal State Management Integration Tests]]
- [[TDD Tests for Modal Agent & Intent Classifier Bugs (PR #5225)]]
