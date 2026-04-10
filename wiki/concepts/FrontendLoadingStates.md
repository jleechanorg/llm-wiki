---
title: "Frontend Loading States"
type: concept
tags: [frontend, user-experience, loading-states, javascript]
sources: []
last_updated: 2026-04-08
---

## Description
Design pattern for providing contextual feedback during async operations. Instead of generic spinners, the UI displays operation-specific messages to keep users informed.

## Key Principles
- **Contextual messages**: Different messages for different operations (loading, saving, new campaign, etc.)
- **Visual feedback**: Smooth opacity transitions and CSS animations
- **Consistent integration**: Global window.loadingMessages object for all components

## Related Patterns
- [[LoadingMessages]] — specific implementation for contextual messages
- [[TASK-005b]] — task that implemented this pattern
