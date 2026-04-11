---
title: "Integration Tests for Modal State Management"
type: source
tags: [python, testing, modal-agent, integration-tests, tdd]
source_file: "raw/test_modal_integration.py"
sources: ["modal-agent-intent-classifier-tdd-tests", "modal-state-management-test-utilities"]
last_updated: 2026-04-08
---

## Summary
Integration tests validating cross-modal interactions, flag pollution prevention, routing vs injection consistency, and modal priority/mutual exclusion in the game system.

## Key Claims
- **Cross-modal flag clearing**: Exiting level-up should clear character_creation_in_progress to prevent recapture by character creation lock
- **Stale flag defense**: Exiting character creation should clear any stale level-up flags
- **Modal priority**: When multiple modal flags are set, only one should actually be active
- **Routing-injection consistency**: Both routing and injection logic must check for stale level_up_in_progress=False flag

## Key Connections
- Related to [[TDD Tests for Modal Agent & Intent Classifier Bugs (PR #5225)]]
- Related to [[Modal State Management Test Utilities]]
