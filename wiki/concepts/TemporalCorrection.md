---
title: "Temporal Correction"
type: concept
tags: [game-state, temporal, firestore]
sources: []
last_updated: 2026-04-08
---

## Description
Mechanism in world_logic.py for handling backward time jumps in game state. When player input causes temporal violations (going back in time), the system attempts corrections.

## Key Behavior
- MAX_TEMPORAL_CORRECTION_ATTEMPTS limits retry attempts
- build_temporal_warning_message generates user-facing warnings
- Bug exists where warning falsely claims success when max attempts exceeded

## Related
- [[Temporal Correction Misleading Success Message Bug]] — tests the misleading success message bug
- [[Temporal Correction Loop Tests]] — related testing
