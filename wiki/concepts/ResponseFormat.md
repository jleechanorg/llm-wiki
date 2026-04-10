---
title: "Response Format"
type: concept
tags: [game-state, json, response, llm-api]
sources: ["game-state-examples"]
last_updated: 2026-04-08
---

## Description
The JSON schema for LLM responses in WorldArchitect.AI, defining the structure of narrative generation responses including session headers, narrative text, planning blocks, and tool requests.

## Schema Fields
| Field | Type | Description |
|-------|------|-------------|
| session_header | string | Formatted player status string |
| resources | string | Current resource tracking |
| narrative | string | Generated story text |
| tool_requests | array | Dice roll requests for combat |
| planning_block | object | Thinking, context, choices for player |
| dice_rolls | array | Completed dice roll results |
| dice_audit_events | array | Audit trail for dice integrity |
| entities_mentioned | array | Entity names in narrative |
| location_confirmed | string | Verified location |
| state_updates | object | Pending state changes |

## Response Types
- **Combat Phase**: Includes tool_requests for dice rolling
- **Non-Combat**: Standard narrative response with choices

## Connections
- [[SessionHeader]] — session_header field specification
- [[DiceMechanics]] — tool_requests for combat dice
- [[PlanningBlock]] — player choice framework
- [[GameStateExamples]] — primary source for format examples
