---
title: "Continuity Checking"
type: concept
tags: [narrative, validation, consistency, production]
sources: []
last_updated: 2026-04-08
---

## Definition
Validation mechanism that ensures previously noted entity physical states (such as injuries, emotional indicators, or equipment) are maintained consistently across subsequent narrative generations.

## How It Works
1. Stores entity physical_markers from previous states
2. On new narrative generation, checks if mentioned entities still reference those markers
3. Issues warnings when markers disappear without narrative explanation

## Example
If an entity was marked with "bandaged ear" in a previous turn, the continuity checker ensures either:
- The bandage is still referenced in the new narrative, OR
- A narrative event explains the change ( bandage removed, injury healed)

## Purpose
Prevents narrative desynchronization where characters appear with inconsistent physical states across turns.

## Related Concepts
- [[EntityContext]] — stores physical_markers for continuity
- [[NarrativeSyncValidator]] — implements continuity checking
- [[ValidationResult]] — reports continuity issues as warnings
