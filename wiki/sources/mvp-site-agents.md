---
title: "Agent Architecture"
type: source
tags: [agents, architecture, mode-routing, semantic-classification]
sources: []
last_updated: 2026-04-14
---

## Summary

Agent architecture for WorldArchitect.AI handling different interaction modes. Provides class hierarchy: BaseAgent -> FixedPromptAgent (GodMode, Planning, Info, Rewards) -> StoryModeAgent/CombatAgent. Features semantic intent classifier using FastEmbed (BAAI/bge-small-en-v1.5) for routing user input to appropriate agents. Priority-based agent selection with state-based overrides.

## Key Claims

- **Agent Selection Priority**: (1) GodModeAgent (admin), (2) Character creation completion, (3) CampaignUpgradeAgent (state-based), (4) CharacterCreationAgent (state-based), (5) PlanningAgent (explicit override), (6) Semantic Intent Classifier (primary brain with FastEmbed), (7) API explicit mode, (8) StoryModeAgent (default)
- **Semantic Intent Classification**: Uses FastEmbed BAAI/bge-small-en-v1.5 to classify intent, can route to: CombatAgent, RewardsAgent, InfoAgent, CharacterCreationAgent, LevelUpAgent, CampaignUpgradeAgent, PlanningAgent, FactionManagementAgent
- **Prompt Order Invariants**: master_directive MUST be first; game_state and planning_protocol MUST be consecutive
- **Agent Class Hierarchy**: BaseAgent (ABC) -> FixedPromptAgent (god_mode, think, info, rewards) -> StoryModeAgent/CombatAgent
- **Time Advancement**: `advances_time` property determines if agent progresses world clock (default True, override for GodMode, Planning, Info, CharacterCreation, Rewards, DeferredRewards)
- **Prompt Order Validation**: Runtime validation of REQUIRED_PROMPT_ORDER against invariants, raises ValueError on violation

## Key Quotes

> "Semantic Intent Classifier (PRIMARY BRAIN): Routes based on semantic analysis of user input"

> "master_directive MUST be first (establishes authority)"

> "game_state and planning_protocol MUST be consecutive (anchors schema)"

## Connections

- [[AgentPrompts]] — prompt building utilities
- [[SemanticIntentClassification]] — FastEmbed-based intent routing
- [[AgentModeDetection]] — mode detection logic
- [[PromptOrder]] — prompt ordering constraints

## Contradictions

- None identified