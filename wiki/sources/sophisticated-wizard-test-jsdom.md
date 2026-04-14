---
title: "Sophisticated Red/Green Test for Campaign Wizard Reset"
type: source
tags: [testing, red-green, tdd, jsdom, browser-simulation, campaign, wizard, javascript]
source_file: "raw/campaign-wizard-reset-test.js"
sources: []
last_updated: 2026-04-08
---

## Summary
Node.js test class using jsdom to simulate a realistic browser environment for testing campaign wizard reset functionality. Validates the complete user workflow: create campaign → complete → navigate back → click "Start Campaign". Tests DOM manipulation, form reset, spinner removal, and step navigation.

## Key Claims
- **Test Environment**: JSDOM simulates browser with realistic DOM structure
- **Test Target**: CampaignWizard class and wizard state management
- **Files Tested**: campaign-wizard.js and app.js
- **User Workflow Validated**: Full journey from campaign creation through completion and reset
- **Performance**: Tests run in Node.js without browser overhead

## Key Test Cases
- Wizard container exists after enable() is called
- Wizard has content after reset (not empty)
- No spinner present in reset state
- Wizard has step navigation
- Form reset behavior after campaign completion
- DOM element visibility toggling

## Connections
- [[CampaignWizard]] — class being tested
- [[jsdom]] — library providing browser simulation
- [[RedGreenTDD]] — testing methodology
