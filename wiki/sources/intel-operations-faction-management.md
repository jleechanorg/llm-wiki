---
title: "Intel Operations for WorldAI Faction Management"
type: source
tags: [intel, faction-management, game-mechanics, spy-operations, detection, formulas]
source_file: "raw/intel-operations-faction-management.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python implementation of intel operation formulas for the WorldAI Faction Management system. Provides functions for spy deployment, detection risk calculation, and intel success tier determination with configurable modifiers and difficulty scaling.

## Key Claims
- **Detection Risk Formula**: Base 30% + target defenses (shadow networks × 2%, wards × 5%) - attacker bonuses (spies × 1%, spymaster × 2%, lineage intrigue × 3%), clamped between 5-90%
- **Intel Success Tiers**: FAILURE, PARTIAL, SUCCESS, CRITICAL based on spy strength vs target defense ratio with difficulty multipliers (easy: 0.5, medium: 1.0, hard: 1.5, legendary: 2.0)
- **Deterministic Testing**: Provides deterministic variant of intel success calculation for test reproducibility
- **Typed Results**: IntelResult TypedDict returns tier, detection status, intel gathered amount, and message

## Key Functions
- `calculate_detection_risk()` — computes detection probability with defender/attacker modifiers
- `is_detected()` — rolls against detection risk
- `calculate_intel_success()` — determines success tier with randomness
- `calculate_intel_success_deterministic()` — deterministic version for testing

## Connections
- [[WorldAI]] — game platform providing faction management system
- [[FactionMinigame]] — strategic layer where intel operations are used
- [[DualModeCampaignSystem]] — combines with personal adventures

## Contradictions
- []
