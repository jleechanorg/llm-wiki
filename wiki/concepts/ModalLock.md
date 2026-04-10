---
title: "Modal Lock"
type: concept
tags: [modal, locking, character-creation, level-up]
sources: []
last_updated: 2026-04-08
---

## Summary
Modal lock is a state management pattern that prevents certain actions while a modal (like character creation or level-up) is active. Enforced in world_logic.py via _enforce_character_creation_modal_lock.

## Key Claims
- **Stale Flags**: level_up_complete and level_up_cancelled must be cleared when new level-up becomes available
- **Active Label**: level_up label added to active_modal_labels when modal in progress
- **Protected Flags**: Certain flags preserved during level-up to prevent blocking

## Related
- [[LevelUp]] — game mechanic that uses modal lock
- [[CharacterCreationModal]] — modal being enforced
- [[PR5282]] — PR implementing modal lock
