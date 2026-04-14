---
title: "mvp_site entity_validator"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/entity_validator.py
---

## Summary
Enhanced post-generation validation with retry logic (Option 2 Enhanced). Validates AI output for missing entities and provides retry suggestions. Consolidates utility functions for filtering 'Unknown' entities, entity presence detection with regex patterns, and retry management.

## Key Claims
- EntityValidator class validates entity presence, analyzes presence types (PHYSICALLY_PRESENT, MENTIONED_ABSENT, IMPLIED_PRESENT, AMBIGUOUS)
- EntityRetryManager implements smart retry strategies with max_retries configuration
- filter_unknown_entities removes 'Unknown' placeholder from validation lists
- ValidationResult provides unified format with backward compatibility fields

## Connections
- [[GameState]] — validates entities present in generated narrative against game state
- [[Validation]] — EntityValidator is used alongside NarrativeSyncValidator for comprehensive validation