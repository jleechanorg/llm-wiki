---
title: "Internal Mode Rejection Tests"
type: source
tags: [python, testing, agents, mode-routing, security]
source_file: "raw/test_internal_mode_rejection.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite verifying that INTERNAL modes cannot be forced via the API 'mode' parameter. Internal modes (combat, rewards, info, character_creation, dialog_heavy) must be selected automatically by the system based on state or classifier decisions, not user input. Only user-facing modes (think, god) are allowed to be explicitly requested.

## Key Claims
- **Internal mode rejection**: Modes like combat, rewards, info, character_creation, and dialog_heavy are rejected when passed via the API and fall back to StoryMode
- **Case-insensitive rejection**: Internal modes are rejected regardless of casing (e.g., "COMBAT" also fails)
- **User-facing modes allowed**: Think mode and God mode CAN be explicitly requested via the API
- **Think mode requires explicit parameter**: Prefix text alone (e.g., "Please think carefully...") is no longer sufficient to trigger think mode

## Key Quotes
> "Verify that INTERNAL modes cannot be forced via the API 'mode' parameter. Internal modes must be selected automatically by the system (state or classifier)."

## Connections
- [[StoryModeAgent]] — fallback when internal modes are rejected
- [[GodModeAgent]] — allowed user-facing mode
- [[PlanningAgent]] — allowed user-facing mode
- [[IntentClassifier]] — determines mode automatically
- [[get_agent_for_input]] — function that enforces mode restrictions

## Contradictions
- None identified — this test validates security boundaries around mode forcing
