---
title: "God Mode Return Story"
type: concept
tags: [god-mode, mode-switching, choices]
sources: [god-mode-planning-blocks-tests]
last_updated: 2026-04-08
---

## Definition
Mandatory choice in every God mode planning block that allows players to exit God mode and return to normal story progression.

## Requirements
- ID must be "god:return_story"
- Must have switch_to_story_mode set to true
- Should have "safe" risk_level

## Behavior
When selected, transitions the game from God mode back to story/character mode.

## Related Concepts
- [[ChoiceIdPrefix]] — Naming requirement
- [[PlanningBlock]] — Container structure
- [[God Mode]] — Parent mode

## Source
Derived from [[God Mode Planning Blocks Tests]]
