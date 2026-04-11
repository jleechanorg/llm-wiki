---
title: "Dice Strategy Selection"
type: source
tags: [dice, strategy, gemini, cerebras, openrouter, tool-calling]
source_file: "raw/dice-strategy-selection.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Module that centralizes dice rolling strategy selection between Gemini code_execution (single API call with Python dice) and universal two-phase tool calling (server-executed tool_requests). Separated from constants.py to maintain unit testability and avoid logic mixing with configuration.

## Key Claims
- **Strategy Options**: code_execution uses Python for dice within single Gemini call; native_two_phase uses server-executed tool_requests
- **Provider Routing**: Gemini uses code_execution; Cerebras/OpenRouter use native_two_phase
- **Design Separation**: Kept separate from mvp_site/constants.py to avoid constants becoming a logic grab-bag

## Key Quotes
> "Kept separate from mvp_site/constants.py to avoid turning constants into a grab-bag of logic and to make unit testing clearer."

## Connections
- [[Gemini]] — uses code_execution strategy
- [[Cerebras]] — uses native_two_phase strategy  
- [[OpenRouter]] — uses native_two_phase strategy
- [[Constants]] — related configuration module

## Contradictions
- []
