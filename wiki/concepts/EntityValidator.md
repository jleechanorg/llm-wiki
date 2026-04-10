---
title: "EntityValidator"
type: concept
tags: [validation, entity-tracking, narrative, production]
sources: []
last_updated: 2026-04-08
---

## Definition
Centralized entity validation component in WorldArchitect.AI that serves as the single source of truth for entity presence logic in narrative generation. Other validators (like NarrativeSyncValidator) delegate to this component rather than implementing duplicate logic.

## Key Responsibilities
- Validate presence of entities in generated narrative text
- Check expected entities against actual narrative content
- Support location-based and previous-state-based validation
- Provide confidence scores for validation results

## Related Concepts
- [[NarrativeSyncValidator]] — delegates to EntityValidator
- [[EntityContext]] — provides contextual data for validation
- [[ValidationResult]] — structured output format

## Usage
Used by llm_service.py and other narrative generation components to ensure characters, locations, and objects are properly tracked throughout a game session.
