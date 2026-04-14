---
title: "test_agents.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Comprehensive test suite for all agent classes in the architecture: BaseAgent (abstract), StoryModeAgent, GodModeAgent, CombatAgent, DialogAgent, HeavyDialogAgent, CharacterCreationAgent, SpicyModeAgent, RewardsAgent, DeferredRewardsAgent, InfoAgent, PlanningAgent, and FactionManagementAgent. Tests cover routing logic, prompt configuration, time advancement, and game state matching.

## Key Claims
- BaseAgent is abstract with REQUIRED_PROMPTS and OPTIONAL_PROMPTS class attributes
- Time-advancing agents (StoryModeAgent, CombatAgent, DialogAgent, HeavyDialogAgent, FactionManagementAgent) set advances_time=True
- Non-advancing agents (GodModeAgent, InfoAgent, PlanningAgent, CharacterCreationAgent, RewardsAgent) set advances_time=False
- DialogAgent routing uses semantic classifier (classify_intent) exclusively, not keyword matching on planning blocks
- Exact commands like "enable_faction_minigame" override dialog context deterministically

## Connections
- [[mvp-site-agents]] — canonical location for all agent classes
- [[mvp-site-agent_prompts]] — defines PromptBuilder for instruction compilation
- [[mvp-site-narrative_response_schema]] — defines VALID_RISK_LEVELS