---
title: "mvp_site dual_mode"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/dual_mode.py
---

## Summary
Dual-Mode Campaign System integrating D&D adventure gameplay with faction management. Tracks time at two scales (personal minutes/hours vs strategic days/weeks), mode switching between /adventure and /faction, and attention triggers for crises/reminders/opportunities.

## Key Claims
- CampaignMode enum: ADVENTURE (personal) vs FACTION (strategic)
- TriggerUrgency enum: LOW, MEDIUM, HIGH, CRITICAL
- TriggerType enum: crisis events (SIEGE, ASSASSINATION), neglect warnings, opportunities (ALLIANCE_OFFER, TRADE_PROPOSAL)
- Trigger dataclass with id, type, urgency, message, created_turn, expires_turn

## Connections
- [[FactionMinigame]] — faction strategic mode integration
- [[CombatSystem]] — personal adventure mode
