---
title: "test_agent_architecture_end2end.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
End-to-end integration tests for the agent architecture through the Flask API. Tests verify agent routing based on user input (regular inputs to StoryModeAgent, GOD MODE: prefix to GodModeAgent), prompt loading for each agent type, mode switching within a session, and SpicyModeAgent routing with intent classifier integration.

## Key Claims
- API correctly routes different input types: regular inputs -> story mode, GOD MODE: prefix -> god mode, THINK: prefix -> think mode
- StoryModeAgent has master_directive, game_state, DND_SRD as required prompts; narrative and mechanics as optional
- GodModeAgent has master_directive, god_mode, game_state, DND_SRD, mechanics as required; excludes narrative prompts
- Mode switching works bidirectionally between story mode and god mode in same session

## Connections
- [[mvp-site-agents]] — defines StoryModeAgent, GodModeAgent, SpicyModeAgent
- [[mvp-site-intent_classifier]] — classifies user intent to route to correct agent
- [[mvp-site-constants]] — defines prompt types and modes