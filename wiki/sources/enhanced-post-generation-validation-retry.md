---
title: "Enhanced Post-Generation Validation with Retry"
type: source
tags: [python, entity-validation, ai-output-validation, retry-logic, narrative-generation]
source_file: "raw/enhanced-post-generation-validation-retry.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing post-generation validation for AI outputs with entity presence checking and retry logic. Implements the EntityValidator class that scans generated narratives for missing entities and provides actionable retry suggestions to improve entity tracking in story generation.

## Key Claims
- **Entity Presence Detection**: Classifies entity presence as physically_present, mentioned_absent, implied_present, or ambiguous
- **Unified ValidationResult**: Dataclass with backward compatibility fields for both legacy and new validation formats
- **Advanced Pattern Matching**: Pre-compiled regex patterns for detecting absent references, location transitions, and physical state changes
- **Retry Logic**: Provides concrete suggestions for fixing missing entity issues rather than just reporting failures

## Key Quotes
> "Enhanced post-generation validator that checks for missing entities and provides retry logic for improved entity tracking"

## Connections
- [[EntityValidator]] — main class for validating entity presence
- [[ValidationResult]] — unified result format with backward compatibility
- [[EntityPresenceType]] — enum for presence classification
- [[filter_unknown_entities]] — utility from entity_utils for filtering placeholder entities
- [[is_unknown_entity]] — utility for detecting Unknown placeholders

## Contradictions
- None identified
