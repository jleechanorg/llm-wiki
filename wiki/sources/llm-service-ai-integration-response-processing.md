---
title: "LLM Service - AI Integration and Response Processing"
type: source
tags: [gemini, ai-service, story-generation, prompt-construction, entity-tracking, token-management]
source_file: "raw/llm-service-ai-integration-response-processing.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Comprehensive AI service integration module for WorldArchitect.AI handling story generation, prompt construction, entity tracking, and response processing. Implements a multi-agent architecture supporting story mode, god mode, and combat mode with Gemini AI backend.

## Key Claims
- **Multi-Agent Architecture**: BaseAgent abstract class with StoryModeAgent, GodModeAgent, and CombatAgent subclasses for different interaction modes
- **Gemini AI Backend**: Uses Google Generative AI SDK for story generation with model selection
- **PromptBuilder Integration**: Constructs system instructions via agent_prompts module with load order prioritization
- **Entity Tracking**: EntityPreloader and EntityInstructionGenerator for pre-loading context and creating entity-specific instructions
- **Token Limit Management**: FIXED token limit management to prevent backstory cutoffs
- **Turn/Scene Terminology**: Distinct counting systems (story_entry_count, sequence_id, user_scene_number) for story progression

## Key Classes
- **BaseAgent**: Abstract base class for all agents
- **StoryModeAgent**: Agent for narrative storytelling (character mode)
- **GodModeAgent**: Agent for administrative commands (god mode)
- **CombatAgent**: Agent for active combat encounters
- **PromptBuilder**: Constructs system instructions and prompts
- **LLMResponse**: Custom response object with parsed data
- **EntityPreloader**: Pre-loads entity context for tracking
- **EntityInstructionGenerator**: Creates entity-specific instructions

## Agent Architecture
Each agent has focused subset of system prompts in load order:
- StoryModeAgent: master_directive → game_state → debug → narrative/mechanics → dnd_srd → continuation reminder → optional world
- GodModeAgent: master_directive → god_mode → game_state → mechanics → dnd_srd → debug
- CombatAgent: auto-selected when in_combat=true

## Turn/Scene Counting Systems
- **story_entry_count / turn_number**: Internal counter of ALL story entries (user + AI), calculated as len(story_context) + 1
- **sequence_id**: Absolute position in story array, every entry gets incrementing ID
- **user_scene_number**: User-facing "Scene #X" counter, ONLY increments for AI responses

## Connections
- [[LLMResponse Class for Gemini API Responses]] — custom response object referenced in this service
- [[Structured JSON Request to Gemini API]] — request handling for Gemini API calls
- [[Game State Management Protocol]] — game state context for prompt construction
- [[EntityTracking]] — entity tracking system integrated with this service

## Contradictions
- []
