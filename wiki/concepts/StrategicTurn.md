---
title: "Strategic Turn"
type: concept
tags: [time, turn-based, faction, strategy]
sources: ["dual-mode-campaign-system-dnd-faction-integration"]
last_updated: 2026-04-08
---

## Definition
The primary time unit in FACTION mode, representing 7 in-game days. Used for tracking strategic decisions, resource accumulation, and neglect thresholds.

## Configuration
- **turn_duration_days**: 7 days per strategic turn (configurable)
- **neglect_reminder_threshold**: 3 turns before reminder appears
- **neglect_warning_threshold**: 5 turns before warning appears

## Usage
Strategic turns advance when the player issues faction orders. Each turn advances the in-game calendar by turn_duration_days. The system tracks when the player last issued orders and generates [AttentionTriggers](AttentionTriggers.md) if thresholds are exceeded.

## Related Concepts
- [DualModeCampaignSystem](DualModeCampaignSystem.md) — parent system
- [CampaignMode](CampaignMode.md) — FACTION mode time unit
- [AttentionTriggers](AttentionTriggers.md) — neglect warning generation
- [DeferredRewardsProtocol](DeferredRewardsProtocol.md) — turn-based reward tracking
