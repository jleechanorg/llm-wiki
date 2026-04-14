---
title: "mvp_site extract_sariel_prompts"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/extract_sariel_prompts.py
---

## Summary
Script to extract the first 10 LLM prompts from Sariel campaign for integration testing. Loads campaign data, extracts initial setup prompt and player interaction prompts with context (location, timestamp, expected entities).

## Key Claims
- SarielPromptExtractor class for campaign data extraction
- extract_initial_prompt() creates initial campaign setup prompt (god mode)
- extract_player_prompts() extracts first 10 player interaction prompts with context
- Handles alternative file paths for campaign data lookup

## Connections
- [[EntityTracking]] — expected_entities context extraction
