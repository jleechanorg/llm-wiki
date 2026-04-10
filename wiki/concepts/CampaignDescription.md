---
title: "Campaign Description"
type: concept
tags: [campaign, text-field, truncation]
sources: [dragon-knight-description-length-tests]
last_updated: 2026-04-08
---

The narrative text field describing a campaign's setting, plot, and characters. In the [[DragonKnight]] campaign, the description exceeds 1000 characters, requiring special handling for:
- Storage and transmission
- Preview display (via [[Truncation]])
- Form data collection

## Requirements
- Must include key characters and setting details
- Must be handleable by [[FormDataCollection]]
- Must display properly when truncated

## Related Pages
- [[CampaignWizard]] - handles description
- [[DragonKnight]] - example campaign
- [[Truncation]] - display behavior
