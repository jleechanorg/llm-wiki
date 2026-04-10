---
title: "Intel Success Tiers"
type: concept
tags: [game-mechanics, outcomes, faction-management, intel]
sources: []
last_updated: 2026-04-08
---

Four-tier classification system for intel operation outcomes in WorldAI Faction Management.

## Tier Definitions
1. **FAILURE** — Effective spy strength < 50% of target defense
2. **PARTIAL** — Effective spy strength < 100% of target defense
3. **SUCCESS** — Effective spy strength < 150% of target defense
4. **CRITICAL** — Effective spy strength ≥ 150% of target defense

## Difficulty Modifiers
- Easy: 0.5× defense
- Medium: 1.0× defense (default)
- Hard: 1.5× defense
- Legendary: 2.0× defense

Implemented in [[IntelOperationsFactionManagement]] via `calculate_intel_success()`.
