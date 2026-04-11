---
title: "Static Assets Directory"
type: source
tags: [frontend, assets, worldarchitect, html, javascript, css]
source_file: "raw/static-assets-directory.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Documents the frontend assets directory structure for WorldArchitect.AI, including HTML templates, JavaScript modules, CSS stylesheets, and a comprehensive theme system with 5 themes (light, dark, fantasy, cyberpunk).

## Key Claims
- **SPA Entry Point** — index.html serves as the main HTML template and Single Page Application entry with responsive Bootstrap layout
- **Core Application Logic** — app.js (~2,000+ lines) handles view navigation, campaign management, game interaction, and authentication state
- **API Communication Layer** — api.js provides HTTP client with authentication token management, error handling, and retry logic
- **Firebase Authentication** — auth.js integrates Firebase for Google OAuth, token management, and session handling
- **Modular JavaScript** — 9 feature modules including campaign-wizard.js, theme-manager.js, and component-enhancer.js
- **5 Theme System** — Base theme with light, dark, fantasy, and cyberpunk variants using CSS custom properties
- **Component-Specific Styles** — Separate CSS directories for components, features, and themes

## Directory Structure
```
static/
├── index.html              # SPA entry point
├── app.js                  # Core application logic (~2,000 lines)
├── api.js                  # API communication layer
├── auth.js                 # Firebase authentication
├── style.css               # Main stylesheet
├── css/                    # Component-specific styles
├── js/                     # Modular JavaScript components (9 modules)
├── styles/                 # Feature-specific stylesheets
└── themes/                 # Theme variants (5 themes)
```

## Core Modules

### app.js
Main public methods:
- `showView(viewName)` - Navigate between application views
- `resetNewCampaignForm()` - Reset campaign creation form
- `loadDragonKnightCampaignContent()` - Load default campaign template
- `setupCampaignTypeHandlers()` - Configure campaign type selection

### api.js
Main public methods:
- `makeApiCall(endpoint, options)` - Generic API request handler
- `getCampaigns()` - Fetch user campaigns
- `createCampaign(data)` - Create new campaign
- `sendInteraction(campaignId, input)` - Send user input to AI

### auth.js
Main public methods:
- `initializeAuth()` - Initialize Firebase authentication
- `signInWithGoogle()` - Google OAuth integration
- `signOut()` - User logout
- `getCurrentUser()` - Get current user state

## Connections
- [[WorldArchitect]] — the web application this static directory serves
- [[Single Page Application]] — architectural pattern used by index.html
- [[Theme System]] — CSS-based theming with 5 variants
- [[Firebase Authentication]] — auth.js integrates with Firebase for user management
- [[Campaign Creation Wizard]] — js/campaign-wizard.js provides multi-step form interface

## Contradictions
- None identified
