---
title: "Modal Priority"
type: concept
tags: [modal-agent, state-management, architecture]
sources: ["modal-state-management-integration-tests"]
last_updated: 2026-04-08
---

## Definition
The system must define a clear priority order when multiple modal flags are set simultaneously (e.g., level_up_in_progress=True and character_creation_in_progress=True).

## Current Behavior
Level-up typically takes precedence over character creation when both flags are present.

## Related Tests
- [[Modal State Management Integration Tests]]
- [[TDD Tests for Modal Agent & Intent Classifier Bugs (PR #5225)]]
