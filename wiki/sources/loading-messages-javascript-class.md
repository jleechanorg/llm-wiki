---
title: "LoadingMessages JavaScript Class"
type: source
tags: [javascript, loading, animation, campaign-wizard, message-rotation]
source_file: "raw/loading-messages-javascript-class.md"
sources: ["loading-messages-css-task-005b", "interactive-features-milestone-4"]
last_updated: 2026-04-08
---

## Summary
JavaScript class implementing contextual loading message rotation for the campaign wizard. Supports multiple message contexts (newCampaign, interaction, loading, saving) with automatic 3-second message cycling and inline/overlay detection.

## Key Claims
- **Context-Based Message Sets**: Four distinct message pools for different UI states (newCampaign with 8 messages, interaction with 8, loading with 6, saving with 4)
- **Message Rotation**: Uses setInterval to cycle through messages every 3000ms with fade animations
- **Automatic Element Detection**: getMessageElement() checks for loading-overlay or loading-spinner visibility
- **Fade Animation**: 200ms delay between message changes for smooth transitions
- **Global Export**: Exposes window.loadingMessages for use in app.js

## Key Quotes
> `this.messages = { newCampaign: [...], interaction: [...], loading: [...], saving: [...] }` — message context pools

> `setInterval(() => { this.currentIndex = (this.currentIndex + 1) % messages.length; }, 3000)` — rotation every 3 seconds

## Connections
- [[LoadingMessagesCSS]] — CSS counterpart providing overlay and spinner styling
- [[CampaignWizard]] — main consumer of loading messages
- [[InteractiveFeatures]] — milestone that includes this feature

## Contradictions
- []
