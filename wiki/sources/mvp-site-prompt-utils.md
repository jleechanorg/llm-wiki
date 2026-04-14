---
title: "mvp_site prompt_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/prompt_utils.py
---

## Summary
Pure utility functions for campaign prompt building shared between world_logic.py and tests. Extracted to avoid import-unsafe dependencies and code duplication.

## Key Claims
- _convert_and_format_field() formats field values, converting literal escape sequences to actual characters
- _build_campaign_prompt() builds campaign prompt from character, setting, description components
- Falls back to random character/setting generation when no input provided for testing

## Connections
- [[PromptEngineering]] — campaign prompt building utilities