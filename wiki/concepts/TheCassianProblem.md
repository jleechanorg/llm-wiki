---
title: "The Cassian Problem"
type: concept
tags: [entity-tracking, failure-pattern, sariel, llm-bug]
sources: [sariel-llm-responses-entity-tracking-analysis]
last_updated: 2026-04-08
---

## Description
A documented entity tracking failure pattern in the Sariel campaign system where NPCs explicitly referenced by the player in their input completely disappear from AI-generated narratives.

## Specific Case
- **Input**: "ask for forgiveness. tell cassian i was scared and helpless"
- **Expected**: Narrative includes both Sariel AND Cassian
- **Actual**: Only Sariel appears; Cassian completely absent
- **Success Rate**: 0% (0/1 tests)

## Root Cause
The LLM fails to maintain NPC presence when:
1. Player directly references the NPC by name
2. NPC has emotional/significant context
3. NPC is not a domain owner or player character

## Impact
This is a critical game-breaking bug - players cannot have meaningful interactions with referenced NPCs because those NPCs disappear from the narrative entirely.

## Related Concepts
- [[EntityTracking]] - broader tracking system
- [[NPCDisappearancePattern]] - related failure mode


## Related Entities
- [[Cassian]] - affected NPC
- [[Sariel]] - player character
