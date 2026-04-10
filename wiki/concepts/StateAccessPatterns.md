---
title: "State Access Patterns"
type: concept
tags: [testing, game-state, nested-access, defensive-programming]
sources: []
last_updated: 2026-04-08
---

Design patterns for accessing nested or polymorphic game state structures. The faction_state_util module demonstrates several patterns:

1. **Attribute Access**: Direct `.attribute` access on Mock objects
2. **Dict Access**: Key-based `dict[key]` access
3. **Nested Access**: Chained `obj.attr.nested_attr` access
4. **Wrapper Unwrapping**: Extracting from data wrapper objects
5. **Precedence Rules**: When multiple paths exist, one takes priority

## Testing Approach
Unit tests validate each access pattern with Mock objects, ensuring defensive handling of missing keys, None values, and type mismatches.
