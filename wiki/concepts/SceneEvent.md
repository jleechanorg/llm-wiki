---
title: "Scene Event"
type: concept
tags: [game-mechanics, narrative-rendering, player-facing]
sources: [living-world-advancement-protocol]
last_updated: 2026-04-08
---

## Definition
A game event that MUST be rendered in the player narrative the same turn it is generated. Scene events represent player-facing occurrences like companion requests, messenger arrivals, road encounters, and quest offerings.

## Types
- `companion_request`: Companion speaks in-character
- `messenger`: NPC arrival with news
- `road_encounter`: Random encounter on travel
- `quest_offered`: Quest offered to player

## Rendering Requirements
**CRITICAL**: When `scene_event.type` is any of the above, the event must appear in narrative text this same turn. The `state_updates.scene_event` entry is required, but omitting the narrative rendering is prohibited.

## Visibility Contract
Scene events are never "off-screen bookkeeping" - they represent the living world's direct interface with the player. They must be rendered faithfully with available dialog, action, or speaker details.

## Relationship to Other Concepts
- [[LivingWorld]]: The broader system that generates scene events
- [[WorldEvent]]: Container structure that may include scene events
- [[BackgroundEvent]]: Events not directly player-facing