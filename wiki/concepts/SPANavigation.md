---
title: "SPA Navigation"
type: concept
tags: [single-page-application, client-side-routing, re-initialization]
sources: []
last_updated: 2026-04-08
---

SPA (Single Page Application) navigation refers to client-side page transitions that don't trigger full page reloads. When users navigate to settings in a SPA context, the settings controls must be re-initialized since DOM elements are recreated.

## Challenge
- Traditional DOMContentLoaded only fires on initial page load
- SPA navigation creates new DOM elements dynamically
- Event listeners must be reattached to new elements

## Solution
- `window.initializeSettingsControls()` function
- Callable after SPA navigation completes
- Reattaches listeners and reloads settings data

## Related Pages
- [[Settings Page JavaScript Functionality]] — provides re-initialization function

## Connections
- DOM Manipulation — underlying mechanism
- Event Delegation — alternative pattern
- Client-Side Routing — context
