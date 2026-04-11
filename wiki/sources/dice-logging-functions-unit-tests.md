---
title: "Dice Logging Functions Unit Tests"
type: source
tags: [python, testing, dice-integrity, logging]
source_file: "raw/test_dice_logging_functions.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for dice module logging functions that validate narrative dice detection logging, dice fabrication check logging with debug toggle behavior, fabrication violation alerts, and pre/post detection context logging. Tests ensure logging is conditional on debug flags and uses appropriate log levels.

## Key Claims
- **Narrative Dice Detection Logging**: `log_narrative_dice_detected()` only logs when dice patterns are found in narrative text
- **Fabrication Check Debug Toggle**: `log_dice_fabrication_check()` uses warning level when debug_enabled=True, debug level otherwise
- **Fabrication Violation Alerts**: Dedicated logging for code execution and narrative dice fabrication violations
- **Conditional Context Logging**: Pre/post detection context and results only log when debug_enabled=True

## Key Quotes
> "DICE_NARRATIVE_DETECTED: Dice patterns found in narrative text." — indicates dice found in narrative
> "🚨 DICE_FABRICATION_DETECTED: Found dice in response but no tool/code execution evidence!" — fabrication alert
> "🎲 CODE_EXEC_FABRICATION: Code was executed but random.randint() not found - dice values are fabricated" — code execution violation

## Connections
- [[dice-integrity-module-tests]] — related to dice integrity validation
- [[code-execution-evidence-extraction-rng-verification-tests]] — validates RNG verification logic

## Contradictions
- None identified
