---
title: "Stale Flag"
type: concept
tags: [state-management, bug, flag, detection]
sources: []
last_updated: 2026-04-08
---

## Description
State management anti-pattern where boolean flags retain stale values after their purpose is complete. In modal management, a stale flag can cause incorrect routing decisions.

## Example
After level-up modal completes:
- `level_up_in_progress` should be set to `False`
- If not cleared, system thinks level-up is still in progress
- Related to [[REV-0g1y]] stale flag handling fix


## Prevention
- Clear flags explicitly on modal completion
- Use sentinel values (None) vs booleans for tri-state
- Test for both true AND false conditions

## Connections
- [[REV-0g1y]] — fixed stale flag detection
- [[REV-439p]] — also addresses flag handling
- [[GameState]] — manages flag lifecycle
