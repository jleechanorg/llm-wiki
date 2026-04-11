---
title: "WorldArchitect.AI Frontend App.js — Core UI Logic"
type: source
tags: [frontend, javascript, worldarchitect, ui, navigation, bootstrap, firebase]
source_file: "raw/worldarchitect-ai-frontend-app-js-core-ui-logic.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Core JavaScript module for WorldArchitect.AI frontend handling view navigation, state management, and UI interactions. Manages 4 primary views (auth, dashboard, newCampaign, game), implements rate limiting modals with countdown timers, handles streaming client connections, and integrates Bootstrap tooltips and Firebase settings.

## Key Claims
- **View State Management**: Controls 4 views (auth, dashboard, newCampaign, game) with show/hide transitions
- **Rate Limit Modal**: Dynamic countdown timer showing reset time in hours/minutes or "momentarily"
- **Streaming Client**: Handles real-time streaming element updates with instant scroll behavior
- **BYOK Provider Detection**: Checks custom LLM provider keys via /api/settings endpoint
- **Bootstrap Integration**: Initializes tooltips on mode selection buttons via data-bs-toggle
- **Session Storage**: Manages BYOK CTA dismissal state across sessions

## Key Quotes
> "Helper function for scrolling — uses 'instant' to bypass scroll-behavior:smooth so rapid streaming chunk updates don't lag behind the bottom"

## Connections
- [[Bootstrap]] — tooltip initialization for UI components
- [[Firebase]] — settings retrieval via /api/settings
- [[WorldArchitect.AI]] — parent application using this frontend code
- [[Rate Limiting]] — modal display logic with countdown timers
- [[View Transitions]] — fade animations between view states

## Contradictions
- None identified
