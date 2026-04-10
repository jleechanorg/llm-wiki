---
title: "REV-439p"
type: entity
tags: [pr, level-up, modal-lock, bug-fix]
sources: []
last_updated: 2026-04-08
---

## Description
Pull request addressing level-up modal lock bypass vulnerability. The issue allowed users to bypass the level-up modal when only `level_up_pending=True` was set without `level_up_in_progress`.

## Related Issues
- Fixes modal bypass when `level_up_pending=True` alone is set
- Enables `rewards_pending.level_up_available=True` to activate modal lock
- Related to [[REV-0g1y]] which addressed stale flag handling

## Connections
- [[LevelUpAgent]] — agent that receives modal lock routing
- [[GetAgentForInput]] — function that performs routing logic
