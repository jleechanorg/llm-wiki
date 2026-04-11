---
title: "System Instructions Map"
type: source
tags: [worldarchitect, system-instructions, prompt-engineering, agent-architecture]
sources: []
source_file: worldarchitect.ai-docs-system_instructions_map.md
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary

Comprehensive documentation of WorldArchitect.AI's hierarchical system instruction architecture, mapping all prompt files, their assembly mechanisms, agent type configurations, and critical invariants that must be preserved.

## Key Claims

- **Hierarchical Prompt Architecture**: Multiple prompt files loaded in specific order depending on active agent mode, with earlier prompts establishing authority over later ones
- **PromptBuilder Orchestration**: `PromptBuilder` class in `mvp_site/agent_prompts.py` is the central orchestrator for assembling system instructions
- **Core Prompts (Always Loaded)**: `master_directive.md` (loading hierarchy, conflict resolution), `game_state_instruction.md` (JSON protocol, state schemas), `dnd_srd_instruction.md` (D&D 5E rules authority)
- **Mode-Specific Prompts**: narrative, mechanics, character_template, god_mode, living_world, combat, rewards - each loaded based on active agent mode
- **Dynamic Injection**: Game state, directives, and identity blocks are injected at runtime
- **Living World Triggers**: Background world events generated every N turns (configurable, default every 3 turns)
- **Five Agent Types**: StoryModeAgent, CombatAgent, GodModeAgent, InfoAgent, RewardsAgent - each uses different prompt stacks

## Key Quotes

> "Key Principles: Earlier prompts establish authority over later ones" — Prompt hierarchy invariant

> "The PromptBuilder class in mvp_site/agent_prompts.py is the central orchestrator for this assembly" — Core architecture

## Connections

- [[WorldArchitect.AI]] — the platform using this architecture
- [[PromptBuilder]] — the class that orchestrates prompt assembly

## Contradictions

- None identified