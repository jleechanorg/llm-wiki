---
title: "Single Page Application"
type: concept
tags: [architecture, frontend, web]
sources: [static-assets-directory]
last_updated: 2026-04-08
---

## Overview
Single Page Application (SPA) is an architectural pattern where web pages load once and dynamically update content without full page reloads. WorldArchitect.AI uses this pattern via index.html.

## Key Characteristics
- **Single HTML Entry Point**: One index.html serves the entire application
- **Dynamic Content**: JavaScript updates DOM based on user interactions
- **View Navigation**: app.js handles showView() for switching between views
- **State Management**: Client-side state for authentication, campaigns, and game state
- **Responsive Bootstrap**: Uses Bootstrap for layout and responsive design

## WorldArchitect Implementation
- static/index.html - Main template with dynamic view switching
- static/app.js - Core logic for view navigation and state management
- static/api.js - Asynchronous API communication without page reloads

## Related Concepts
- [[Theme System]] - Dynamic theme switching in SPA
- [[Firebase Authentication]] - Client-side auth state management
- [[Campaign Creation Wizard]] - Multi-step form without navigation
