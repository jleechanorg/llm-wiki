---
title: "Choice Button"
type: concept
tags: [ui-element, interactive-fiction, player-input]
sources: [planning-block-choice-buttons-styles]
last_updated: 2026-04-08
---

An interactive UI element that allows players to select a predefined action or enter a custom response. Choice buttons are the primary input mechanism for player agency in interactive narrative experiences.

## Button Types
- **Standard Choice** — Predefined options with ID and description
- **Custom Choice** — Dashed border styling for player input
- **Custom Action** — Always-visible input field for freeform response

## States
- **Default** — Standard appearance with hover highlight
- **Hover** — Background color shift, border emphasis
- **Active/Pressed** — Darker background feedback
- **Disabled** — Reduced opacity when waiting for response

## Connected Concepts
- [[PlanningBlock]] — The container for choice buttons
- [[NarrativeDirectives]] — Requires player input handling
- [[GameMechanicsProtocol]] — Enforces choice-based progression
