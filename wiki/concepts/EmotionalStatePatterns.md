---
title: "Emotional State Patterns"
type: concept
tags: [narrative, emotion-detection, pattern-matching, game-mechanics]
sources: []
last_updated: 2026-04-08
---

## Definition
Dictionary in NarrativeSyncValidator mapping emotional states to keyword patterns for detecting character emotions in generated narrative text.

## Defined Patterns
- **grief**: ["mourning", "grieving", "sorrowful", "bereaved"]
- **anger**: ["furious", "enraged", "angry", "wrathful"]
- **fear**: ["terrified", "afraid", "fearful", "frightened"]
- **guilt**: ["guilty", "ashamed", "remorseful"]

## Purpose
Enables narrative generation systems to detect and track character emotional states, supporting more emotionally consistent storytelling and enabling emotional arcs to develop naturally.

## Related Concepts
- [[EntityContext]] — stores emotional_state field
- [[NarrativeSyncValidator]] — maintains the patterns dictionary
- [[DialogAgent]] — uses emotional tracking for narrative consistency
