---
title: "Agent Architecture End-to-End Integration Test"
type: source
tags: [python, testing, unittest, integration-test, agent-architecture]
source_file: "raw/agent-routing-schema-validation-tests.md"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test for the agent-based architecture in WorldArchitect. Tests StoryModeAgent vs GodModeAgent selection and behavior through the full application stack, verifying agent selection based on user input, correct system instruction building per agent type, and mode detection functionality.

## Key Claims
- **Agent Selection**: get_agent_for_input correctly selects StoryModeAgent, GodModeAgent, or SpicyModeAgent based on user input
- **System Instruction Building**: Each agent builds appropriate system instructions for its mode
- **Mode Detection**: GOD MODE: prefix detection works end-to-end across the full application stack
- **LLM Integration**: Both StoryModeAgent and GodModeAgent integrate correctly with LLM services through PromptBuilder

## Key Quotes
> "This test suite verifies the complete flow of agent-based mode handling, including mode detection, system instruction building, and integration with the PromptBuilder class" — test purpose statement
> "God mode inputs generally bypass classifier due to prefix priority" — explains god mode routing logic

## Connections
- [[StoryModeAgent]] — handles narrative character interactions
- [[GodModeAgent]] — handles administrative "god mode" commands
- [[SpicyModeAgent]] — handles adult content mode
- [[PromptBuilder]] — constructs prompts from prompt files
- [[IntentClassifier]] — determines user intent for agent routing

## Contradictions
- None identified
