---
title: "mvp_site dice_strategy"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/dice_strategy.py
---

## Summary
Centralizes dice rolling strategy selection between code_execution (Gemini 3.x single-call Python dice) and native_two_phase (server-executed tool_requests for Cerebras/OpenRouter).

## Key Claims
- DICE_STRATEGY_CODE_EXECUTION = "code_execution" — Gemini 3.x single call with Python code
- DICE_STRATEGY_NATIVE_TWO_PHASE = "native_two_phase" — server executes tool_requests
- get_dice_roll_strategy() selects strategy based on model/provider

## Connections
- [[DiceMechanics]] — strategy selection for dice rolling
- [[LLMIntegration]] — provider-specific dice execution
