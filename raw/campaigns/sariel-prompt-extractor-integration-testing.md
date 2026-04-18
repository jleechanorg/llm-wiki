---
title: "Sariel Prompt Extractor for Integration Testing"
type: source
tags: [python, testing, prompt-extraction, campaign-data, integration]
source_file: "raw/sariel-prompt-extractor.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python script for extracting the first 10 LLM prompts from the Sariel campaign for integration testing. Includes the initial campaign setup prompt and player interaction prompts with expected state updates and metadata.

## Key Claims
- **Initial Setup Prompt**: Creates a D&D campaign with House Arcanus member Sariel in a medieval fantasy setting with political intrigue
- **Player Interaction Extraction**: Extracts first 10 player interaction prompts with context including location, timestamp, and expected entities
- **Metadata Tracking**: Marks interaction #2 as the "Cassian problem" — a significant interaction in the campaign
- **Alternative Path Handling**: Gracefully handles path variations in campaign data file names

## Key Functions
- `load_campaign_data`: Loads JSON campaign data with fallback path resolution
- `extract_initial_prompt`: Creates initial campaign setup prompt with player character, NPCs, and location
- `extract_player_prompts`: Extracts player interaction prompts with mode detection
- `format_prompts_for_testing`: Formats prompts for integration test consumption
- `save_prompts`: Outputs prompts as JSON with metadata

## Connections
- [[Sariel]] — campaign protagonist and player character
- [[House Arcanus]] — noble house the player character belongs to
- [[Cassian]] — referenced as a significant problem in interaction #2
- [[Integration Testing]] — the extracted prompts are designed for this purpose
