---
title: "Internal Modes"
type: concept
tags: [agents, mode-routing, security]
sources: [internal-mode-rejection-tests]
last_updated: 2026-04-08
---

## Definition

Internal modes are agent modes that cannot be explicitly requested via the API 'mode' parameter. They must be automatically selected by the system based on game state or intent classification.

## Examples


- **MODE_COMBAT** — combat resolution mode
- **MODE_REWARDS** — encounter rewards mode
- **MODE_INFO** — information lookup mode
- **MODE_CHARACTER_CREATION** — character creation mode
- **MODE_DIALOG_HEAVY** — dialogue-intensive scenes

## Why They Are Internal

These modes depend on complex game state conditions that cannot be safely determined from user input alone:
- Combat requires active combat state
- Rewards requires pending encounter completion
- Character creation requires specific workflow triggers

Allowing users to force these modes could bypass intended game mechanics and create inconsistent state.

## Related

- [[UserFacingModes]] — modes that CAN be explicitly requested
- [[StoryModeAgent]] — fallback when internal modes are rejected
- [[get_agent_for_input]] — function that enforces mode restrictions
