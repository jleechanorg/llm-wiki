---
title: "Form Data Collection"
type: concept
tags: [forms, javascript, user-input]
sources: [dragon-knight-description-length-tests]
last_updated: 2026-04-08
---

Process of gathering user input from HTML forms. In [[CampaignWizard]], tests validate that `collectFormData()` and `populateOriginalForm()` properly handle long [[CampaignDescription]] text (>1000 characters).

## Key Methods
- `collectFormData()` - gathers all form fields
- `populateOriginalForm()` - pre-fills form for editing

## Related Pages
- [[CampaignWizard]] - implements collection
- [[CampaignDescription]] - field being collected
