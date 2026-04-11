---
title: "Modal State Management Test Utilities"
type: source
tags: [python, testing, modal-agent, test-utilities, tdd]
source_file: "raw/test_modal_state_base.py"
sources: ["modal-agent-intent-classifier-tdd-tests"]
last_updated: 2026-04-08
---

## Summary
Base classes and utilities for modal state management testing, providing declarative test scenarios and custom assertion helpers for validating modal behavior in the game system.

## Key Claims
- **ModalTestScenario dataclass**: Declarative test scenario with name, initial_state, action, expected_flags, expected_rewards, and description fields
- **ModalTestBase class**: Base test class with fixtures and custom assertions for semantic modal state checks
- **assert_no_modal_active**: Asserts no modal (character_creation, level_up, campaign_upgrade) is active
- **assert_only_modal_active**: Asserts exactly one specific modal is active
- **assert_stale_flags_cleared**: Asserts stale flags are removed from dict, not just set to False
- **assert_routing_matches_injection**: Validates routing behavior matches injection logic

## Key Connections
- Supports [[TDD Tests for Modal Agent & Intent Classifier Bugs (PR #5225)]] — provides base classes for the TDD test suite
- Related to [[Level-Up Stale Flag Clearing Tests]] — uses assert_stale_flags_cleared for validating flag resets
- Related to [[Level-Up Stale Guard Logic Tests]] — tests guard logic for modal state transitions

## Contradictions
- None identified
