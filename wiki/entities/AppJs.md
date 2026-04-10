---
title: "AppJs"
type: entity
tags: [project, file, javascript, frontend]
sources: []
last_updated: 2026-04-08
---

## Description
Main application JavaScript file containing campaign creation and wizard management logic. Contains form reset behavior at line 56 that resets the new-campaign-form and restores its display after campaign completion.

## Key Functionality
- Form reset logic (line 56): form.reset(), form.style.display = 'block'
- Wizard state checking before enabling
- Campaign creation flow orchestration

## Related Pages
- [[CampaignWizard]] — wizard component managed by app.js
- [[CampaignWizardResetRedGreenTest]] — tests the reset behavior
