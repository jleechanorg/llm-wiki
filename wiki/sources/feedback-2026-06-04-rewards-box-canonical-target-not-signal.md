---
title: "Canonical Level-Up Target Lives in `result.rewards_box`, Not Stream Done Payload"
type: source
tags: ["levelup", "testing", "rewards-box", "worldarchitect-ai", "feedback"]
date: 2026-06-04
source_file: feedback_2026-06-04_rewards_box_canonical_target_not_signal.md
---

## Summary
A no-cap GREEN validation FAILED (`target_level: None`, NO_SIGNAL) as a test-extraction bug. The test read from streaming `done` payload (returned {}) but the model's real output was persisted at `result.rewards_box` (sibling of `game_state`).

## Key Claims
- Streaming `done` payload returned `{}` and omitted `level_up_signal`
- Model's real output at `result.rewards_box`: `current_level=20, new_level=141, resolved_target_level=141, level_up_available=true, source='model'`
- Fix: `post = ctx.get_campaign_state(campaign_id)` then read `post['rewards_box']`
- Fall back chain: `level_up_signal.target_level` (if dict) → turn `rewards_box` → persisted `rewards_box`

## Key Quotes
> Canonical level-up evidence = the `rewards_box` availability layer (5 fields: current_level, new_level, resolved_target_level, level_up_available, source). The streaming `done` payload is NOT a reliable carrier

## Connections
- [[RewardsBox]] — concept
- [[LevelUpTesting]] — test patterns
