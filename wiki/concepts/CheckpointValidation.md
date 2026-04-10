---
title: "Checkpoint Validation"
type: concept
tags: [testing, game-state, validation]
sources: []
last_updated: 2026-04-08
---

## Description
Process of validating save state consistency in game systems. The GameState.validate_checkpoint_consistency() method checks for discrepancies between stored HP values and narrative descriptions, detecting issues like invalid HP states (hp_max=0) and narrative/HP mismatches.

## Key Checks
- Zero HP max detection outside character creation
- HP/narrative mismatch (e.g., narrative describes unconscious but HP is full)
- Type coercion for string HP values
- Graceful handling of None values

## Connections
- [[GameState]] — class that performs checkpoint validation
- [[Character Creation]] — game phase where validation is skipped
- [[DivisionByZero]] — error that validation guards against
