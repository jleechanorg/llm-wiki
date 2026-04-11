---
title: "TDD Tests for CharacterCreationAgent Turn 1 Activation"
type: source
tags: [python, testing, e2e, character-creation, agent-activation]
source_file: "raw/test_character_creation_agent_turn1.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test suite validating that CharacterCreationAgent ALWAYS activates on Turn 1, even when God Mode includes pre-defined character data. Tests cover two scenarios: full God Mode character data (name, class, stats) and minimal God Mode data (just character name and setting).

## Key Claims
- **Turn 1 Activation Invariant**: CharacterCreationAgent must activate on Turn 1 regardless of God Mode pre-defined data
- **Full God Mode Test**: Validates activation with complete character template (Ser Arion val Valerion, Level 1 Paladin, stats)
- **Minimal God Mode Test**: Validates activation with minimal character data (name and setting only)
- **Template Validation**: Ensures campaigns from templates like "My Epic Adventure" require character review before story mode

## Test Setup
- Uses FakeFirestoreClient and FakeLLMResponse for test isolation
- Patches Firestore and LLM service calls
- Creates campaign with god_mode_data and validates Turn 1 response

## Connections
- [[CharacterCreationAgent]] — the agent being tested
- [[Turn1Activation]] — the core invariant being validated
- [[GodMode]] — feature being tested for interaction effects
