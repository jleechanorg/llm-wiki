---
title: "Navigation Handler"
type: concept
tags: [javascript, routing, ui-state]
sources: []
last_updated: 2026-04-08
---

## Description
JavaScript component that manages client-side routing using `history.pushState()` and `handleRouteChange()`. Responsible for updating browser URL without page reload while maintaining application state.


## Key Responsibility
Must preserve UI component states (like wizard enable/disabled) when performing route transitions.
