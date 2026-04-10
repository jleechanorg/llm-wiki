---
title: "MAX_TEMPORAL_CORRECTION_ATTEMPTS"
type: entity
tags: [constant, configuration]
sources: []
last_updated: 2026-04-08
---

## Description
Constant defining the maximum number of temporal correction attempts allowed before the system gives up. When temporal_correction_attempts exceeds this value, the correction is considered failed.

## Context
Used in world_logic.py to determine when to stop attempting temporal corrections and emit a warning message to the user.

## Related
- [[Temporal Correction Misleading Success Message Bug]] — tests bug where message falsely claims success when max attempts exceeded
- [[Temporal Correction Loop Tests]] — related temporal correction testing
