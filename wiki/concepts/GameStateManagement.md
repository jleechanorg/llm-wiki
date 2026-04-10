---
title: "Game State Management"
type: concept
tags: [game-state, protocol, worldarchitect]
sources: [game-state-management-protocol]
last_updated: 2026-04-08
---

Game State Management in WorldArchitect.AI refers to the protocol for maintaining and updating all game state information through structured JSON responses. It encompasses session headers, narrative content, planning blocks, entity tracking, and state updates that must be included in every AI response.

**Key Components**:
- Session header with timestamp, location, status
- Narrative text for player visibility
- Planning block with thinking and choice options
- State updates for internal tracking
- Entity ID system (type_name_### format)

**Related Concepts**:
- [[JSONSchema]] — defines valid response structure
- [[SessionHeader]] — required prefix for responses
- [[EntityTrackingSystem]] — entity ID management
- [[TurnVsScene]] — numbering distinction
