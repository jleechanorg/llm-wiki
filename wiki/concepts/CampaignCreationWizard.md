---
title: "Campaign Creation Wizard"
type: concept
tags: [feature, frontend, user-interface, worldarchitect]
sources: [static-assets-directory]
last_updated: 2026-04-08
---

## Overview
A multi-step form interface for guided campaign setup in WorldArchitect.AI. Implemented as a JavaScript module (js/campaign-wizard.js) that provides step-by-step campaign configuration.

## Key Features
- **Multi-Step Form**: Breaks campaign creation into digestible steps
- **Validation**: Each step validates before proceeding
- **Guided Setup**: User-facing prompts for campaign configuration
- **State Preservation**: Maintains form state across steps

## Module Location
- `static/js/campaign-wizard.js` - Main wizard implementation
- Related: `static/js/interface-manager.js` for modal management

## Workflow
1. User initiates campaign creation
2. Wizard displays step 1 (campaign type selection)
3. User completes each step with validation
4. Final step submits to backend via api.js
5. Campaign created and user redirected to game view

## Related Concepts
- [[WorldArchitect]] - Host application
- [[Single Page Application]] - Enables wizard without page navigation
- [[API Communication]] - api.js handles campaign creation POST
