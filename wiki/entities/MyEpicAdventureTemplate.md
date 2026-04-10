---
title: "My Epic Adventure Template"
type: entity
tags: [template, campaign]
sources: []
last_updated: 2026-04-08
---

## Description
Campaign creation template in the game system that includes pre-defined character data. Used in end-to-end tests to validate CharacterCreationAgent behavior.

## Template Content
- Character: Ser Arion | Setting: World of Assiah
- Full character build with stats, gear, and backstory
- Triggers Turn 1 CharacterCreationAgent activation for user review

## Test Purpose
Validates invariant: users creating campaigns from templates must review their character via CharacterCreationAgent before story mode starts.

## See Also
- [[CharacterCreationAgent]]
- [[CampaignCreation]]
- [[WorldOfAssiah]]
