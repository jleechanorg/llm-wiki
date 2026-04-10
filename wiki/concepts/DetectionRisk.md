---
title: "Detection Risk"
type: concept
tags: [game-mechanics, probability, stealth, risk-calculation]
sources: []
last_updated: 2026-04-08
---

Probability calculation for spy operations being detected by target faction defenses. Uses a formula that balances target defensive capabilities against attacker offensive capabilities.

## Formula Components
- **Base Risk**: 30%
- **Defensive Penalties**: shadow networks × 2%, wards × 5%
- **Offensive Bonuses**: spy count × 1% (capped at 15%), spymaster mod × 2%, lineage intrigue × 3%
- **Clamp**: 5% minimum, 90% maximum

## Usage
Used by [[IntelOperationsFactionManagement]] to determine if spies are detected during intel operations.
