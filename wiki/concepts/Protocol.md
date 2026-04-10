---
title: "Protocol (Python)"
type: concept
tags: [python, typing, structural-subtyping]
sources: [shared-type-definitions]
last_updated: 2026-04-08
---

## Description
Python typing construct enabling structural subtyping (duck typing with type checking). Defines interfaces that classes can implement without explicit inheritance.

## Usage in WorldArchitect.AI
Two Protocol definitions:
- **DatabaseService**: defines get_campaign, update_campaign, delete_campaign
- **AIService**: defines generate_response, validate_response

## Benefits
- Interface contracts without inheritance
- Multiple implementation support
- Type-safe service substitution
- Enables dependency injection patterns
