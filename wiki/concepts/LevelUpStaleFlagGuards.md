---
title: "LevelUpStaleFlagGuards"
type: concept
tags: [level-up, stale-flags, modal-routing, rewards-engine]
sources: [level-up-pr6339-verification-status-2026-04-17]
last_updated: 2026-04-17
---

# LevelUpStaleFlagGuards

Guard behavior that prevents stale persisted level-up flags from reactivating modal UI or routing after the canonical XP/rewards signal is gone.

## Rules

- Explicit `level_up_in_progress=False` blocks stale modal reactivation.
- Explicit `level_up_pending=False` blocks stale pending reactivation unless a true in-progress signal is present.
- `rewards_pending.level_up_available=True` remains a canonical positive signal only when corroborated by state or rewards-engine progression.
- Ordinary planning choices must not be converted into level-up planning only because a stale `level_up_in_progress=True` flag exists.

## Related

- [[PR6339]]
- [[LevelUpVerificationStatus]]
- [[RewardsEngine]]
