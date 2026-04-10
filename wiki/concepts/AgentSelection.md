---
title: "Agent Selection"
type: concept
tags: [agent, routing, worldarchitect]
sources: []
last_updated: 2026-04-08
---

## Summary
Agent Selection is the process by which WorldArchitect determines which agent (StoryModeAgent, GodModeAgent, or SpicyModeAgent) should handle a given user input. The selection is made by get_agent_for_input based on input analysis and user settings.

## Selection Logic
1. **Priority Order**: GodModeAgent > SpicyModeAgent > StoryModeAgent
2. **God Mode Detection**: Input starting with "GOD MODE:" routes to GodModeAgent
3. **Spicy Mode Check**: User setting spicy_mode=true routes to SpicyModeAgent
4. **Default**: All other inputs route to StoryModeAgent

## Why Multiple Agents
- **Specialization**: Each agent handles specific interaction types
- **System Instructions**: Agents build different system prompts appropriate to their mode
- **Response Format**: Agents produce different response structures (god_mode_response vs narrative)
- **State Management**: Different agents manage different state update patterns

## Related Concepts
- [[AgentArchitecture]] — overall system design
- [[ModeDetection]] — specific detection of god mode prefix
- [[UserSettings]] — configuration affecting selection (spicy_mode)

## Source References
- [[Agent Architecture End-to-End Integration Test]] — tests agent selection logic
