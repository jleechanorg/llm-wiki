---
title: "ProcessActionUnified"
type: entity
tags: [function, api, world-logic]
sources: ["mode-parameter-type-validation-tests"]
last_updated: 2026-04-08
---

## Summary
Unified async function in mvp_site.world_logic that processes player actions across all game modes. The function accepts a request dict with user_id, campaign_id, user_input, and optional mode parameter.

## Context
- Module: mvp_site.world_logic
- Known bug: mode parameter type validation — accepts dict/list/int/None instead of only string
- Related to: [[LLMRequest validation]] — validates request parameter types

## Key Connections
- Called by: API endpoints processing player actions
- Validates: [[LLMRequest]] parameter types including mode field
