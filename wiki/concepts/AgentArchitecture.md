---
title: "Agent Architecture"
type: concept
tags: [architecture, agent-system, worldarchitect]
sources: []
last_updated: 2026-04-08
---

## Summary
Agent Architecture in WorldArchitect refers to the system of specialized agents that handle different interaction modes. The architecture uses a factory pattern (get_agent_for_input) to select the appropriate agent based on user input characteristics.

## Key Components
- **get_agent_for_input**: Factory function that selects agent based on input analysis
- **StoryModeAgent**: Handles standard narrative interactions
- **GodModeAgent**: Handles administrative commands (GOD MODE: prefix)
- **SpicyModeAgent**: Handles adult content mode (spicy_mode user setting)

## How It Works
1. User input is analyzed by get_agent_for_input
2. Input is checked for GOD MODE: prefix → GodModeAgent
3. User settings checked for spicy_mode → SpicyModeAgent
4. Otherwise → StoryModeAgent
5. Selected agent builds system instructions and processes input
6. Agent integrates with LLM service for response generation

## Related Concepts
- [[AgentSelection]] — the decision process for choosing agents
- [[ModeDetection]] — detecting user intent from input patterns
- [[LLMIntegration]] — service layer all agents use

## Source References
- [[Agent Architecture End-to-End Integration Test]] — validates full stack agent selection and behavior
