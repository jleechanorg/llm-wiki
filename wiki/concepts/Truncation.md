---
title: "Truncation"
type: concept
tags: [text-processing, ui, display]
sources: [dragon-knight-description-length-tests]
last_updated: 2026-04-08
---

Text processing technique that shortens long content for display while indicating there is more. Implemented in [CampaignWizard](CampaignWizard.md)'s `_formatDescription()` method.

## Specification
- Truncates to 50 characters
- Appends "..." to indicate continuation
- Used for [CampaignDescription](CampaignDescription.md) previews

## Related Pages
- [CampaignWizard](CampaignWizard.md) - implements truncation
- [CampaignDescription](CampaignDescription.md) - content being truncated
