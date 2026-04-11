---
title: "End-to-end integration test for DialogAgent"
type: source
tags: [python, testing, integration, dialog-agent, llm, agent-architecture]
source_file: "raw/test_dialog_agent_end2end.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test suite for DialogAgent. Tests verify that DialogAgent is selected for dialog state continuity or explicit dialog mode, builds correct system instructions focused on character/dialog, excludes mechanics/combat/SRD instructions, and integrates correctly with the LLM service.

## Key Claims
- **DialogAgent Selection**: DialogAgent is selected for dialog state continuity or explicit dialog mode
- **System Instructions**: DialogAgent builds correct system instructions focused on character/dialog
- **Exclusion**: DialogAgent excludes mechanics/combat/SRD instructions from its prompts
- **LLM Integration**: Dialog mode integrates correctly with the LLM service
- **Priority Ordering**: Dialog mode ordering works (dialog after rewards, before story mode)

## Key Test Cases
- `test_dialog_agent_selection_dialog_state`: Tests DialogAgent selection when dialog state is active
- `test_dialog_agent_selection_explicit_mode`: Tests DialogAgent selection for explicit dialog mode
- `test_dialog_agent_system_instructions`: Validates system instructions exclude mechanics/combat
- `test_dialog_mode_llm_integration`: Tests full stack LLM integration for dialog
- `test_agent_priority_ordering`: Validates priority ordering (rewards → dialog → story)

## Connections
- [[DialogAgent]] — the agent being tested
- [[StoryModeAgent]] — compared agent for system instruction differences
- [[CombatAgent]] — compared agent for mechanics exclusion
- [[GodModeAgent]] — compared agent for priority ordering
