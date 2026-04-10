---
title: "Dual-Mode Campaign System"
type: concept
tags: [campaign-system, dual-mode, dnd, faction, game-design]
sources: ["dual-mode-campaign-system-dnd-faction-integration"]
last_updated: 2026-04-08
---

## Definition
A game system that alternates between personal D&D adventure gameplay and strategic faction management. Players switch between direct character action (adventure mode) and high-level kingdom/organization command (faction mode) using /adventure and /faction commands.

## Time Scales
- **Personal Mode**: Minutes/hours — used for combat, exploration, dialogue
- **Strategic Mode**: Days/weeks — 1 strategic turn equals 7 in-game days

## Core Components
- [[CampaignMode]] — ADVENTURE or FACTION focus
- [[AttentionTriggers]] — system for crises and neglect warnings
- [[StrategicTurn]] — time unit for faction mode

## Usage
Players use /adventure to enter personal mode (direct character control) or /faction to enter strategic mode (kingdom/organization management). The system tracks time differently in each mode and generates attention triggers when switching between modes.

## Related Concepts
- [[DungeonsAndDragons]] — base rules for adventure mode
- [[CombatSystemProtocol]] — initiative and turn structure
- [[DeferredRewardsProtocol]] — turn-based reward tracking
