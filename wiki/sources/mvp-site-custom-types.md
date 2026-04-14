---
title: "mvp_site custom_types"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/custom_types.py
---

## Summary
Shared type definitions for WorldArchitect.AI using TypedDict for Firebase data structures and Protocol for interface contracts. Provides type safety across CampaignData, StateUpdate, EntityData, MissionData, and service protocols.

## Key Claims
- TypedDicts: CampaignData, StateUpdate, EntityData, MissionData, ApiResponse, LLMRequest, LLMResponse
- Type aliases: UserId, CampaignId, EntityId, SessionId, Timestamp, JsonValue, JsonDict
- DatabaseService Protocol: get_campaign, update_campaign, delete_campaign interface contract
- AIService Protocol: generate_response, validate_response interface contract
- Valid literals: VALID_ENTITY_TYPES, VALID_CAMPAIGN_STATES, VALID_LOG_LEVELS

## Connections
- [[GameState]] — TypedDict definitions for game state structures
