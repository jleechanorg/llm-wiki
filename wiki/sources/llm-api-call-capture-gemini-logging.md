---
title: "LLM API Call Capture — Gemini Prompt/Response Logging"
type: source
tags: [worldarchitect, testing, llm-capture, api-logging, gemini, campaign]
source_file: "raw/llm-api-call-capture-gemini-logging.json"
sources: []
last_updated: 2026-04-08
---

## Summary
Captures raw LLM API calls from Sariel campaign replay using Gemini 1.5 Flash model. Records full prompt structure including entity manifests, scene metadata, game state, and timeline context. Demonstrates structured prompt engineering with mandatory entity tracking and response format requirements.

## Key Claims
- **Entity Manifest System**: Prompts include mandatory entity lists that must be acknowledged in responses
- **Scene Manifest**: Tracks location, session, turn, and present characters (PCs, NPCs)
- **Game State Integration**: Full game state JSON passed in prompt for context-aware generation
- **Timeline Log**: Previous interaction history included for narrative continuity
- **Response Schema Enforcement**: JSON output required with narrative, entities_mentioned, and location_confirmed fields

## Key Quotes
> "IMPORTANT: The following entities MUST be acknowledged or mentioned in your response as they are present in this scene: Sariel"

> "CRITICAL ENTITY TRACKING REQUIREMENT: You MUST mention ALL characters listed in the manifest above in your narrative"

## Connections
- [[Sariel]] — player character driving the campaign
- [[GeminiProvider]] — model provider for these captures
- [[CampaignWizard]] — campaign creation workflow
- [[NarrativeResponseSchema]] — enforced response format

## Contradictions
- None identified
