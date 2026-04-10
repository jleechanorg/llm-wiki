---
title: "CampaignWizard"
type: entity
tags: [class, javascript, frontend, campaign]
sources: [sophisticated-wizard-test-jsdom]
last_updated: 2026-04-08
---

## Summary
JavaScript class in frontend_v1/js/campaign-wizard.js that manages the campaign creation wizard UI and state. Handles wizard enable/disable, form display, step navigation, and campaign launch. Tested by the sophisticated Red/Green test using jsdom simulation.

## Key Methods
- enable() — shows wizard interface
- launchCampaign() — submits campaign form
- reset state — clears wizard after campaign completion

## Connections
- [[SophisticatedWizardTestJsdom]] — tests this class
- [[CampaignWizardReset]] — related workflow being tested
