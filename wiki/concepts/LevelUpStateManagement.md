---
title: "Level-Up State Management"
type: concept
tags: [state-management, level-up, flags, bug-fix]
sources: ["level-up-stale-flag-tests"]
last_updated: 2026-04-08
---

## Definition
State management patterns for level-up modal transitions in WorldArchitect game logic, handling flag clearing and rewards state cleanup.

## Key Flags
| Flag | Purpose | Bug |
|------|---------|-----|
| level_up_in_progress | Indicates level-up modal is active | Not cleared when new level-up becomes available |
| level_up_complete | Indicates level-up was completed | Properly cleared |
| level_up_cancelled | Indicates level-up was cancelled | Properly cleared |
| character_creation_in_progress | Indicates character creation modal | Not cleared on level-up modal exit |
| rewards_pending | Signals rewards UI to display | Not fully removed on exit, leaving stale keys |

## Related Concepts
- [[ModalStateTransitions]] — modal enter/exit patterns
- [[StateFlagPatterns]] — general flag lifecycle management
- [[RewardsContext]] — _has_rewards_context() function that checks rewards_pending
