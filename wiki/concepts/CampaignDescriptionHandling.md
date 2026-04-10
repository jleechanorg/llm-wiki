---
title: "Campaign Description Handling"
type: concept
tags: [ui, form-handling, truncation]
sources: []
last_updated: 2026-04-08
---

## Description
Pattern for handling long campaign descriptions in the campaign wizard UI. Includes truncation for preview displays and full preservation for form data storage.

## Key Behaviors
- **Definition**: Campaign descriptions stored as static class properties (e.g., DEFAULT_DRAGON_KNIGHT_DESCRIPTION)
- **Truncation**: Preview displays truncate to ~50 characters with ellipsis
- **Full Storage**: Form data collection preserves full description (1000+ characters)
- **Population**: Form populator correctly sets textarea values from data objects

## Connections
- [[CampaignWizard]] — class implementing this pattern
