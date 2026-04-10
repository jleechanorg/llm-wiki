---
title: "Type Alias"
type: concept
tags: [python, typing]
sources: [shared-type-definitions]
last_updated: 2026-04-08
---

## Description
Type alias in Python creates a shorthand for complex types, improving code readability.

## Usage in WorldArchitect.AI
Seven type aliases defined:
- UserId = str
- CampaignId = str
- EntityId = str
- SessionId = str
- Timestamp = datetime | float | int
- JsonValue = str | int | float | bool | None | dict | list
- JsonDict = dict[str, JsonValue]

## Benefits
- Reduces repetitive type annotations
- Documents intent of type usage
- Easy to modify type in one place
