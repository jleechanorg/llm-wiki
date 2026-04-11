---
title: "Dual-Mode Campaign System: D&D + Faction Integration"
type: source
tags: [campaign-system, dnd, faction, time-tracking, mode-switching, triggers]
source_file: "raw/dual-mode-campaign-system.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module implementing Phase 1 of a dual-mode campaign system that combines personal D&D adventures with strategic faction management. Features time tracking with different scales (minutes/hours for adventure mode vs days/weeks for strategic mode), mode switching via commands (/faction, /adventure), and an attention trigger system for crisis events and neglect warnings.

## Key Claims
- **Dual Time Scales**: Personal Mode tracks minutes/hours (combat, exploration, dialogue) while Strategic Mode uses days/weeks (1 turn = 7 in-game days)
- **Mode Switching**: Commands /faction and /adventure switch between focus modes
- **Attention Triggers**: System for crises (Strategic -> Personal) and neglect warnings (Personal -> Strategic)
- **Trigger Urgency Levels**: LOW ( ignorable), MEDIUM (should address soon), HIGH (needs attention this session), CRITICAL (interrupts adventure immediately)
- **Trigger Types**: Siege, Assassination, Discovery (Strategic -> Personal); Neglect Reminder/Warning, Enemy Approaching, Treasury Critical (Personal -> Strategic); Alliance Offer, Trade Proposal, Building Complete (Opportunities)

## Architecture
- CampaignMode Enum: ADVENTURE and FACTION modes
- TriggerUrgency Enum: LOW, MEDIUM, HIGH, CRITICAL
- TriggerType Enum: 14 distinct trigger types across three categories
- Trigger Dataclass: Attention trigger with id, type, urgency, message, creation turn, expiration
- DualModeState Dataclass: State management including strategic turn counter, pending triggers, dismissed trigger tracking, and adventure checkpointing

## Key Configuration
- neglect_reminder_threshold: 3 turns before reminder
- neglect_warning_threshold: 5 turns before warning  
- turn_duration_days: 7 days per strategic turn

## Connections
- [[DungeonsAndDragons]] — D&D rules foundation for Personal Mode
- [[CombatSystemProtocol]] — adventure mode time tracking for combat encounters
- [[DeferredRewardsProtocol]] — strategic turn-based reward tracking

## Contradictions
- None — new module introducing dual-mode paradigm
