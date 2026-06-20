---
title: "LoadingMessages"
type: concept
tags: [frontend, javascript, loading-states, user-experience]
sources: []
last_updated: 2026-04-08
---

## Description
JavaScript class that manages contextual loading messages for different application states. Provides dynamic spinner messages based on the current operation type.

## Message Types
- **newCampaign**: "🎲 Rolling for initiative", "🏰 Building your world"
- **interaction**: "🤔 The DM is thinking"
- **loading**: "📚 Loading your adventure"
- **saving**: "💾 Saving your progress"

## Implementation
- CSS classes: .loading-message, .loading-content
- Properties: opacity transitions for smooth UI
- Integration: window.loadingMessages global object

## Connections
- [TASK-005b](../entities/TASK-005b.md) — task this feature was implemented for
- [FrontendLoadingStates](FrontendLoadingStates.md) — broader concept of loading UX
- [[LoadingSpinnerMessagesTests]] — tests validating this feature
